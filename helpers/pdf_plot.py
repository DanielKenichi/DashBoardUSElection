import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


class PDFPlot:
    def __init__(self, n: int, mean: float, std_deviation: float):
        self.n = n
        self.mean = mean
        self.std_deviation = std_deviation

    def plot(self, desired_percentile: float, real_data: np.array) -> plt.Figure:
        counts, bin_edges = np.histogram(real_data, bins=50, density=True)
        x = (bin_edges[:-1] + bin_edges[1:]) / 2  # centros dos bins
        probList = counts

        fig, ax = plt.subplots(figsize=(14, 8))

        ax.plot(x, probList, c='green', linewidth=1.5, linestyle=':')
        ax.fill_between(x, probList, facecolor='blue', alpha=0.3)

        x_percent = np.percentile(real_data, desired_percentile * 100)

        mask = x < x_percent
        ax.fill_between(x[mask], np.array(probList)[mask], facecolor='darkred')

        k = np.searchsorted(x, x_percent)
        if k > 0 and k < len(x):
            x0, x1 = x[k - 1], x[k]
            y0, y1 = probList[k - 1], probList[k]
            fraction = (x_percent - x0) / (x1 - x0)
            y_interp = y0 + fraction * (y1 - y0)
            ax.fill_between([x0, x_percent], [y0, y_interp], facecolor='darkred')

        ax.set_xlabel('Valor', fontsize=22)
        ax.set_ylabel('Densidade de Probabilidade', fontsize=22)
        ax.set_title(f'PDF, $N(\\mu={self.mean}, \\sigma={self.std_deviation}) \quad X = {x_percent:.2f}$', fontsize=14, weight='bold')
        ax.axvline(x_percent, linewidth=1, linestyle='-.', color='darkred')

        ax.text(0.95, 0.85, f"X = {x_percent:.2f}", transform=ax.transAxes,
                fontsize=12, color='black', horizontalalignment='right')

        fig.tight_layout()
        return fig
