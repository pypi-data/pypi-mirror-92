import gorilla
from .models import Algorithm, HyperParameter, HyperParameterSetting, Implementation, Run, RunSchema, ModelEvaluation, EvaluationMeasure
from .common import fn_args_as_params, mls_add_param
from .io import log_renku_mls


def autolog():
    import pytorch_lightning as pl
    from pytorch_lightning.core.memory import ModelSummary
    from pytorch_lightning.utilities import rank_zero_only

    class MLSPLCallback(pl.Callback):
        def __init__(self):
            self.early_stopping = False
            self.mls = Run(uuid1())

        def on_epoch_end(self, trainer, pl_module):
            """
            Log loss and other metrics values after each epoch
            :param trainer: pytorch lightning trainer instance
            :param pl_module: pytorch lightning base module
            """
            if (pl_module.current_epoch + 1) % every_n_epoch == 0:
                for key, value in trainer.callback_metrics.items():
                    try_mlflow_log(
                        mlflow.log_metric, key, float(value), step=pl_module.current_epoch
                    )

            for callback in trainer.callbacks:
                if isinstance(callback, pl.callbacks.early_stopping.EarlyStopping):
                    self._early_stop_check(callback)

        def on_train_start(self, trainer, pl_module):
            """
            Logs Optimizer related metrics when the train begins
            :param trainer: pytorch lightning trainer instance
            :param pl_module: pytorch lightning base module
            """
            try_mlflow_log(mlflow.set_tag, "Mode", "training")
            mls_add_param(self.mls, "epochs", trainer.max_epochs)

            for callback in trainer.callbacks:
                if isinstance(callback, pl.callbacks.early_stopping.EarlyStopping):
                    self.early_stopping = True
                    self._log_early_stop_params(callback)

            # TODO For logging optimizer params - Following scenarios are to revisited.
            # 1. In the current scenario, only the first optimizer details are logged.
            #    Code to be enhanced to log params when multiple optimizers are used.
            # 2. mlflow.log_params is used to store optimizer default values into mlflow.
            #    The keys in default dictionary are too short, Ex: (lr - learning_rate).
            #    Efficient mapping technique needs to be introduced
            #    to rename the optimizer parameters based on keys in default dictionary.

            if hasattr(trainer, "optimizers"):
                optimizer = trainer.optimizers[0]
                mls_add_param(self.mls, "optimizer_name", type(optimizer).__name__)

                if hasattr(optimizer, "defaults"):
                    mls_add_param(self.mls, optimizer.defaults)

            summary = str(ModelSummary(pl_module, mode="full"))
            tempdir = tempfile.mkdtemp()
            try:
                summary_file = os.path.join(tempdir, "model_summary.txt")
                with open(summary_file, "w") as f:
                    f.write(summary)

                try_mlflow_log(mlflow.log_artifact, local_path=summary_file)
            finally:
                shutil.rmtree(tempdir)

        def on_train_end(self, trainer, pl_module):
            """
            Logs the model checkpoint into mlflow - models folder on the training end
            :param trainer: pytorch lightning trainer instance
            :param pl_module: pytorch lightning base module
            """

            mlflow.pytorch.log_model(pytorch_model=trainer.model, artifact_path="model")

            if self.early_stopping and trainer.checkpoint_callback.best_model_path:
                try_mlflow_log(
                    mlflow.log_artifact,
                    local_path=trainer.checkpoint_callback.best_model_path,
                    artifact_path="restored_model_checkpoint",
                )

        def on_test_end(self, trainer, pl_module):
            """
            Logs accuracy and other relevant metrics on the testing end
            :param trainer: pytorch lightning trainer instance
            :param pl_module: pytorch lightning base module
            """
            try_mlflow_log(mlflow.set_tag, "Mode", "testing")
            for key, value in trainer.callback_metrics.items():
                try_mlflow_log(mlflow.log_metric, key, float(value))

        @staticmethod
        def _log_early_stop_params(early_stop_obj):
            """
            Logs Early Stop parameters into mlflow
            :param early_stop_obj: Early stopping callback dict
            """
            if hasattr(early_stop_obj, "monitor"):
                try_mlflow_log(mlflow.log_param, "monitor", early_stop_obj.monitor)

            if hasattr(early_stop_obj, "mode"):
                try_mlflow_log(mlflow.log_param, "mode", early_stop_obj.mode)

            if hasattr(early_stop_obj, "patience"):
                try_mlflow_log(mlflow.log_param, "patience", early_stop_obj.patience)

            if hasattr(early_stop_obj, "min_delta"):
                try_mlflow_log(mlflow.log_param, "min_delta", early_stop_obj.min_delta)

            if hasattr(early_stop_obj, "stopped_epoch"):
                try_mlflow_log(mlflow.log_param, "stopped_epoch", early_stop_obj.stopped_epoch)

        @staticmethod
        def _early_stop_check(early_stop_callback):
            """
            Logs all early stopping metrics
            :param early_stop_callback: Early stopping callback object
            """
            if early_stop_callback.stopped_epoch != 0:

                if hasattr(early_stop_callback, "stopped_epoch"):
                    try_mlflow_log(
                        mlflow.log_metric, "stopped_epoch", early_stop_callback.stopped_epoch
                    )
                    restored_epoch = early_stop_callback.stopped_epoch - max(
                        1, early_stop_callback.patience
                    )
                    try_mlflow_log(mlflow.log_metric, "restored_epoch", restored_epoch)

                if hasattr(early_stop_callback, "best_score"):
                    try_mlflow_log(
                        mlflow.log_metric, "best_score", float(early_stop_callback.best_score)
                    )

                if hasattr(early_stop_callback, "wait_count"):
                    try_mlflow_log(mlflow.log_metric, "wait_count", early_stop_callback.wait_count)

    def _run_and_log_function(self, original, args, kwargs):
        """
        This method would be called from patched fit method and
        It adds the custom callback class into callback list.
        """
        if not mlflow.active_run():
            try_mlflow_log(mlflow.start_run)
            auto_end_run = True
        else:
            auto_end_run = False

        if not any(isinstance(callbacks, MLSPLCallback) for callbacks in self.callbacks):
            self.callbacks += [MLSPLCallback()]
        result = original(self, *args, **kwargs)
        if auto_end_run:
            try_mlflow_log(mlflow.end_run)
        return result

    @gorilla.patch(pl.Trainer)
    def fit(self, *args, **kwargs):
        """
        Patching trainer.fit method to add autolog class into callback
        """
        original = gorilla.get_original_attribute(pl.Trainer, "fit")
        return _run_and_log_function(self, original, args, kwargs)

    wrap_patch(pl.Trainer, "fit", fit)