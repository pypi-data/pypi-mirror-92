import pandas as pd

def to_excel(report_data, filename):
    """Exports data to Excel file"""
    
    posts_as_dict = report_data.copy()

    for sub in posts_as_dict:
        i = 0
        for post in posts_as_dict[sub]:
            posts_as_dict[sub][i] = posts_as_dict[sub][i].as_dict()     # Stores posts as dict in a new dict
            i += 1

    for sub in posts_as_dict:
        df_report = pd.DataFrame.from_dict(posts_as_dict[sub])
    df_report.to_excel(filename, index=False)
