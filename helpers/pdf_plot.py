import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


class PDFPlot:
    def __init__(self, n: int, mean: float, std_deviation: float):
        self.n = n
        self.mean = mean
        self.std_deviation = std_deviation

    def plot(self, desired_percentile: float) -> plt.Figure:
        probList = []
        x = np.arange(0, self.mean+3 * self.std_deviation, 0.1)

        for xi in x:
            probList.append(norm.pdf(xi, loc=self.mean, scale=self.std_deviation))

        fig = plt.figure(figsize=(24,8))

        plt.subplot(1, 2, 1)
        plt.plot(x,probList,c='green',linewidth=1.5,linestyle=':')
        plt.fill_between(x,probList, facecolor='blue', alpha=0.3)

        # Perceint Point Function, inversa da Cumulative Distribution Function
        x_percent = norm.ppf(desired_percentile, loc=self.mean, scale=self.std_deviation)

        plt.fill_between(np.arange(0,x_percent,0.1), probList[0:len(np.arange(0,x_percent,0.1)+1)], facecolor='darkred')
        plt.xlabel('Valor')
        plt.ylabel('Função Densidade de Probabilidade')
        plt.title(f'PDF, $N(\mu={self.mean}, \sigma={self.std_deviation})$', fontsize=14, weight='bold')
        plt.axvline(x_percent,linewidth=1,linestyle='-.',color='darkred')

        plt.text(x_percent + 2, 0.0005, f"X = {'{:.2f}'.format(x_percent)}", fontsize=12, color='black')

        return fig
