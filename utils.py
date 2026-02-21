import matplotlib.pyplot as plt
import io
import base64
from models import Activity

def generate_activity_plot():
    activities = Activity.query.all()
    categories = {}
    for act in activities:
        categories[act.category] = categories.get(act.category, 0) + act.duration

    plt.figure(figsize=(6,4))
    plt.bar(categories.keys(), categories.values(), color='skyblue')
    plt.xlabel('Kategori')
    plt.ylabel('Totalt antal minuter')
    plt.title('Tid per aktivitet')
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return f"data:image/png;base64,{plot_url}"
