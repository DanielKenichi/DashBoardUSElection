from typing import Tuple
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm, gaussian_kde


class PDFPlot:
    def plot(self, desired_percentile: float, real_data: np.array) -> Tuple[plt.Figure, float]:
        # Ordena os dados
        real_data = np.sort(real_data)
        
        # Calcula a média e o desvio padrão
        mean = np.mean(real_data)
        std_deviation = np.std(real_data)

        # Define os valores de x e calcula a densidade usando a distribuição normal
        x = np.arange(0, mean + 3 * std_deviation, 10)
        probList = [norm.pdf(xi, loc=mean, scale=std_deviation) for xi in x]
        
        # Cria a figura e um único eixo
        fig, ax = plt.subplots(figsize=(16,8))
        
        # Plota a curva e preenche a área sob ela
        ax.plot(x, probList, c='green', linewidth=1.5, linestyle=':')
        ax.fill_between(x, probList, facecolor='blue', alpha=0.3)
        
        # Calcula o percentil desejado e preenche a área até esse valor
        x_percent = norm.ppf(desired_percentile, loc=mean, scale=std_deviation)
        mask = x < x_percent
        ax.fill_between(x[mask], np.array(probList)[mask], facecolor='darkred')
        
        # Define rótulos e título (reduzindo o padding)
        ax.set_xlabel('Valor')
        ax.set_ylabel('Função Densidade de Probabilidade')
        ax.set_title(
            f'PDF, $N(\\mu={mean:.2f}, \\sigma={std_deviation:.2f})$',
            fontsize=14, weight='bold', pad=10
        )
        ax.axvline(x_percent, linewidth=1, linestyle='-.', color='darkred')
        
        # Posiciona o texto usando coordenadas relativas (fixo dentro do eixo)
        ax.text(0.95, 0.90, f"X = {x_percent:.2f}", transform=ax.transAxes,
                fontsize=12, color='black', ha='right')
        
        fig.tight_layout()
        return fig, x_percent
