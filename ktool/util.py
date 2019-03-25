def get_basic(df):
    print(df.info())
    print(df.isnull().sum())
    df.head()

def xgb_plot_features(booster, figsize=(10,14)):
    from xgboost import plot_importance
    fig, ax = plt.subplots(1,1,figsize=figsize)
    return plot_importance(booster=booster, ax=ax)

def boxplot(df, column):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10,4))
    plt.xlim(df[[column]].min(), df[['column']].max()*1.1)
    sns.boxplot(x=df[[column]])
