import pathlib
import matplotlib.pyplot as plt
import pandas as pd

def create_plot_for_benchmark(test_data, name, max_gap):

    plt.rcParams.update({'font.size': 14})

    plt.title(name)    
    fig, ax1 = plt.subplots(figsize=(10,8))
    color = 'tab:blue'
    ax1.set_xticklabels(ax1.get_xticklabels(),rotation=55,ha='right')
    ax1.set_ylabel('Runtime (s)', color=color)
    ax1.set_ylim([0, 60])
    
    time = [0 if t > 60 else t for t in test_data["TIME"]]
    x_labels = [s.replace(f"_options_{name}","") for s in test_data["NAME"]]
    ax1.bar(x_labels,time, width=0.4,label=f"Runtime",color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()  
    color = 'tab:red'
    ax2.set_ylabel('Optimality gap (objective/bound)', color=color)
    ax2.set_ylim([0, max_gap*1.1])
    ax2.bar(x_labels,test_data["GAP"], width=0.4, label=f"Optimality gap",color=color)

    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    pathlib.Path(f'graphs').mkdir(parents=True, exist_ok=True)
    plt.savefig(f'graphs/{name}.png')


results_data = pd.read_csv(f"results.csv", sep = ",")
max_gap = results_data["GAP"].max()

options = ["0","1","2","3","4","Poppy","Trine","Simon","Rakul","Maria"]

for o in options:
    test_data = results_data[results_data["NAME"].str.endswith(o)]    
    create_plot_for_benchmark(test_data, o, max_gap)
    