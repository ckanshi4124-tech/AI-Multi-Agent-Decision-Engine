import mlflow

def setup_mlflow(experiment_name):
    mlflow.set_tracking_uri("file:./mlruns")
    mlflow.set_experiment(experiment_name)