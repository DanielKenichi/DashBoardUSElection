import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


class PDFPlot:
    def __init__(self, n: int, mean: float, std_deviation: float):
        self.n = n
        self.mean = mean
        self.std_deviation = std_deviation

    def plot(self, desired_percentile: float, real_data: np.array) -> plt.Figure:
        # Cálculo do histograma com os dados reais
        counts, bin_edges = np.histogram(real_data, bins=50, density=True)
        x = (bin_edges[:-1] + bin_edges[1:]) / 2  # centros dos bins
        probList = counts

        # Cria uma figura e um único eixo
        fig, ax = plt.subplots(figsize=(14, 8))

        ax.plot(x, probList, c='green', linewidth=1.5, linestyle=':')
        ax.fill_between(x, probList, facecolor='blue', alpha=0.3)

        # Cálculo do percentil utilizando os dados reais
        x_percent = np.percentile(real_data, desired_percentile * 100)

        # Preenche a região até o percentil
        mask = x < x_percent
        ax.fill_between(x[mask], np.array(probList)[mask], facecolor='darkred')

        ax.set_xlabel('Valor', fontsize=22)
        ax.set_ylabel('Densidade de Probabilidade', fontsize=22)
        ax.set_title(f'PDF, $N(\\mu={self.mean}, \\sigma={self.std_deviation}) \quad X = {x_percent:.2f}$', fontsize=14, weight='bold')
        ax.axvline(x_percent, linewidth=1, linestyle='-.', color='darkred')

        # Posiciona o texto relativo ao eixo (usando coordenadas de axes)
        ax.text(0.95, 0.85, f"X = {x_percent:.2f}", transform=ax.transAxes,
                fontsize=12, color='black', horizontalalignment='right')

        fig.tight_layout()
        return fig
