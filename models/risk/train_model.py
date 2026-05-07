from models.risk.train import (
    generate_dataset,
    train_model
)

if __name__ == "__main__":
    df = generate_dataset(
        n_samples=1500
    )

    train_model(df)