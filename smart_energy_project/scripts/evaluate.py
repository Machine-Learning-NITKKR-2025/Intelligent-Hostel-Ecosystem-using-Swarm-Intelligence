"""Evaluation script
- Loads outputs/predictions_*.csv and creates simple plots (true vs pred)
- Saves plots to outputs/
"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

def plot_preds(path, title):
    df = pd.read_csv(path)
    plt.figure(figsize=(10,3))
    plt.plot(df['y_true'].values, label='true')
    plt.plot(df['y_pred'].values, label='pred')
    plt.legend()
    plt.title(title)
    outpng = OUT / (Path(path).stem + '.png')
    plt.savefig(outpng)
    plt.close()
    print('Saved', outpng)

def main():
    for p in OUT.glob('predictions_*'):
        plot_preds(p, p.stem)

if __name__ == '__main__':
    main()
