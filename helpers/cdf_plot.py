from typing import Tuple
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm, gaussian_kde

class CDFPlot:
    def plot(self, desired_percentile: float, real_data: np.array) -> Tuple[plt.Figure, float]:
        # Ordena os dados
        real_data = np.sort(real_data)

        # Calcula a média e o desvio padrão
        mean = np.mean(real_data)
        std_deviation = np.std(real_data)

        # Define os valores de x para o gráfico
        x = np.arange(0, mean + 3 * std_deviation, 10)
        # Calcula os valores da CDF para cada x
        cdf_values = [norm.cdf(xi, loc=mean, scale=std_deviation) for xi in x]

        # Calcula o valor x que corresponde ao percentil desejado
        x_percent = norm.ppf(desired_percentile, loc=mean, scale=std_deviation)
        # Como por definição, norm.cdf(x_percent) ≈ desired_percentile
        cdf_at_x_percent = norm.cdf(x_percent, loc=mean, scale=std_deviation)

        # Cria a figura e um eixo para o gráfico da CDF
        fig, ax = plt.subplots(figsize=(16,8))
        
        # Plota a curva da CDF
        ax.plot(x, cdf_values, c='green', linewidth=1.5, linestyle=':')
        ax.fill_between(x, cdf_values, facecolor='blue', alpha=0.3)
        
        # Define rótulos e título
        ax.set_xlabel('Valor')
        ax.set_ylabel('Função Probabilidade Acumulada')
        ax.set_title(
            f'CDF, $N(\\mu={mean:.2f}, \\sigma={std_deviation:.2f})$',
            fontsize=14, weight='bold', pad=10
        )
        # Adiciona linha vertical e horizontal no ponto do percentil
        ax.axvline(x_percent, linewidth=1, linestyle='-.', color='darkred')
        ax.axhline(cdf_at_x_percent, linewidth=1, linestyle='-.', color='darkred')
        ax.plot(x_percent, cdf_at_x_percent, 'o', color='darkred')
        
        # Anota o valor de P(x <= x_percent) na posição adequada
        ax.text(x_percent + 10, cdf_at_x_percent,
                f'P(x ≤ {x_percent:.2f}) = {cdf_at_x_percent:.2f}',
                fontsize=12, color='black')
        
        fig.tight_layout()
        return fig, x_percent
    