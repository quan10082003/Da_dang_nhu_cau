import pandas as pd

def generate_OD_csv(complete_plan_df: pd.DataFrame) -> pd.DataFrame:
    # 1. Ép kiểu về string để tránh lẫn lộn số và chữ
    df = complete_plan_df.copy()
    df['idO'] = df['idO'].astype(str)
    df['idD'] = df['idD'].astype(str)
    
    # 2. Dùng crosstab
    od_matrix = pd.crosstab(df['idO'], df['idD'])
    return od_matrix

if __name__ == "__main__":
    pass

