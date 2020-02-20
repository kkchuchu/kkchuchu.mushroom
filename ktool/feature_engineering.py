import pandas as pd
import seaborn as sns
from IPython.display import display, HTML
from matplotlib import pyplot as plt
from pandas.api.types import is_numeric_dtype, is_datetime64_any_dtype, is_categorical_dtype
import pandas as pd
from sklearn.linear_model import LogisticRegression
import numpy as np

DEFAULT_IMAGE_HEIGHT = 14
DEFAULT_COLOR_MAP = "YlGnBu"

<<<<<<< HEAD

def run(df: pd.DataFrame, columns: list=None, category_columns: list=[], datetime_columns: list=[], numeric_columns: list=[],
        string_columns: list=[],
        drop_duplicated=False,
        display_heatmap=False, display_duplicated=True, 
        height=DEFAULT_IMAGE_HEIGHT, display=display, color_map=DEFAULT_COLOR_MAP, 
       ):
    if columns is None:
        columns = df.columns

        
    # basic information
    display(df.head())
    display(df.describe())
    print('records count are: ', len(df))
    
    duplicated_count = df.duplicated(subset=columns).sum()
    print('duplicated: ', duplicated_count)
    if display_duplicated and duplicated_count > 0:
        display(df[df.duplicated(subset=columns)])
    
    
    print('null check: ')
    print(df.isnull().sum())
    # TODO fill null
    
    
    # drop duplicate and reset index
    if drop_duplicated:
        # TODO
        assert False

        
    # type convert
    for cat_col in category_columns:
        df[cat_col] = df[cat_col].astype('category')
        
    for col in datetime_columns:
        if is_numeric_dtype(df.dtypes[col]):
            df[col] = df.apply(lambda x: datetime.fromtimestamp(x[col]), axis=1)
        else:
            df[col] = pd.to_datetime(df[col])
            
    for col in string_columns:
        df[col] = df[col].astype('unicode')
    

    # heatmap
    if display_heatmap:
        plt.figure()
        sns.heatmap(df.corr(), annot=True, cmap=color_map)


=======
        
>>>>>>> origin/master
def show(df: pd.DataFrame, display_columns: list=None, show_count=True,
         subimage_column: str=None, hint: str=None,
         height=DEFAULT_IMAGE_HEIGHT, color_map=DEFAULT_COLOR_MAP, display_pairplot=True, diag_kind="kde",
         ):
    '''
    doc: https://seaborn.pydata.org/generated/seaborn.countplot.html
    col is subgraph label
    
    display category dist
    https://seaborn.pydata.org/generated/seaborn.barplot.html
    cont2cont_action: cont2line or cont2cont
    
    plot trend
    Doc: https://seaborn.pydata.org/generated/seaborn.lineplot.html
    
    x: continuous, y:continuous
    Doc: https://seaborn.pydata.org/generated/seaborn.relplot.html
    
    date only be x (can not be y)
    '''
    if display_columns is None:
        display_columns = df.columns 
    date_columns = [c for c in display_columns if is_datetime64_any_dtype(df.dtypes[c])]
    non_date_columns = [c for c in display_columns if not is_datetime64_any_dtype(df.dtypes[c])]
        
    xy2actions = {
        'is_cont': { 
            'is_cate': cont2cate,
            'is_cont': cont2line,
        },
        'is_cate' : {
            'is_cate': None,
            'is_cont': cate2cont, 
        },
    }
    
    # pairplot
    if display_pairplot:
        plt.figure()
        sns.pairplot(df, hue=hint, palette=color_map, diag_kind=diag_kind, height=height)
    
    
    # non datetime type columns
    for i, x_c in enumerate(non_date_columns):
        for y_c in non_date_columns[i+1:]:
            x_key = _which_type(df.dtypes[x_c])
            y_key = _which_type(df.dtypes[y_c])
            y_action_list = xy2actions[x_key]
            show_image = y_action_list[y_key]
            if show_image is not None:
                print(x_c, y_c)
                show_image(df, x_c, y_c, hint=hint, subimage_column=subimage_column, height=height)
   
    # datetime type columns
    print('datetime display')
    for x in date_columns:
        y = [c for c in non_date_columns if is_numeric_dtype(df.dtypes[c])]
        show_x_is_datetime(df, x, y, show_count=show_count,
                           subimage_column=subimage_column, hint=hint,
                           height=height, color_map=color_map,
                           )
    
    # count
    if show_count:
        xcount2action = {
            'is_cont': cont2count,
            'is_cate': cate2count,
        }
        for x_c in non_date_columns:
            print('show count', x_c)
            x_key = _which_type(df.dtypes[x_c])
            show_image = xcount2action[x_key]
            show_image(df, x_c, hint=hint, subimage_column=subimage_column, height=height)


def show_x_is_datetime(df: pd.DataFrame, x, y, show_count=True,
                       subimage_column: str=None, hint: str=None,
                       height=DEFAULT_IMAGE_HEIGHT, color_map=DEFAULT_COLOR_MAP,
                       ):
    for y_c in y:
        if not is_numeric_dtype(df.dtypes[y_c]):
            print(y_c, 'should be numeric, but is', df.dtypes[y_c])
        print(y_c)
        cont2line(df, x, y_c, hint=hint, subimage_column=subimage_column, height=height)
    
    if show_count:
        cont2count(df, x, hint=hint, subimage_column=subimage_column, height=height)
        
        
def cate2count(df: pd.DataFrame, x, hint=None, subimage_column=None, height=DEFAULT_IMAGE_HEIGHT):
    plt.figure()
    sns.catplot(data=df, x=x, 
                       hue=hint, col=subimage_column,
                       kind='count', height=height)


def cont2count(df: pd.DataFrame, x, hint=None, subimage_column=None, height=DEFAULT_IMAGE_HEIGHT):
    d = df[x].value_counts().reset_index()
    y = x + '_count'
    d.rename(columns={'index': x, x: y}, inplace=True)
    return cont2cont(d, x, y, hint=hint, subimage_column=subimage_column, height=height)
    

def cate2cont(df: pd.DataFrame, x, y, hint=None, subimage_column=None, height=DEFAULT_IMAGE_HEIGHT):
    plt.figure()
    sns.catplot(data=df, x=x, y=y, hue=hint, kind='bar', col=subimage_column)


def cont2cate(df: pd.DataFrame, x, y, hint=None, subimage_column=None, height=DEFAULT_IMAGE_HEIGHT):
    plt.figure()
    sns.catplot(data=df, x=y, y=x, hue=hint, kind='bar', col=subimage_column)


def cont2line(df: pd.DataFrame, x, y, hint=None, subimage_column=None, height=DEFAULT_IMAGE_HEIGHT):
    plt.figure()
    sns.lineplot(data=df, x=x, y=y, hue=hint)


def cont2cont(df: pd.DataFrame, x, y, hint=None, subimage_column=None, height=DEFAULT_IMAGE_HEIGHT):
    plt.figure()
    sns.scatterplot(data=df, x=x, y=y, hue=hint, col=subimage_column, height=height)


def top(df, column: str, n: int=5):
    return df.sort_values(column, ascending=False).head(n)


def sort(df, by):
    return df.sort_values(by=by, ascending=False)


def get_top_what1_of_what2(df, what1: str, what2: str, top=6):
    return df.groupby(by=[what1])[what2] \
        .sum() \
        .reset_index() \
        .sort_values(by=[what2], ascending=False).head(top)[what1].values


def _which_type(dtype):
    if is_numeric_dtype(dtype):
        return 'is_cont'
    elif is_categorical_dtype(dtype):
        return 'is_cate'
    else:
        return None


def odd_ratio(df, x, y):
    """
    https://dasanlin888.pixnet.net/blog/post/34469402
    
    odd ratio could consider as independent as well when odd == 1
    https://en.wikipedia.org/wiki/Odds_ratio
    """
    # TODO
    clf = LogisticRegression(C=1e5)
    X = df[x].values.reshape(200,1)
    clf.fit(X,y)
    np.exp(clf.coef_)
    pass


def cont2cont_point(df: pd.DataFrame):
    """[summary]
    
    Arguments:
        df {[type]} -- [description]
    """
    # TODO
    sns.scatterplot(df)
