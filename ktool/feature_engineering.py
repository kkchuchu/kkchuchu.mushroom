import pandas as pd
import seaborn as sns
from IPython.display import display, HTML
from matplotlib import pyplot as plt
from pandas.api.types import is_numeric_dtype, is_datetime64_any_dtype, is_categorical_dtype


DEFAULT_IMAGE_HEIGHT = 14
DEFAULT_COLOR_MAP = "YlGnBu"


def run(df: pd.DataFrame, columns: list=None, category_columns: list=[], datetime_columns: list=[], numeric_columns: list=[],
        drop_duplicated=False,
        display_heatmap=False, display_duplicated=True, 
        height=DEFAULT_IMAGE_HEIGHT, display=display, color_map=DEFAULT_COLOR_MAP
       ):
    if columns is None:
        columns = df.columns

        
    # basic information
    display(df.head())
    display(df.describe())
    print('records count are: ', len(df))
    
    duplicated_count = df.duplicated().sum()
    print('duplicated: ', duplicated_count)
    if display_duplicated and duplicated_count > 0:
        display(df[df.duplicated()])
    
    
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
    

    # heatmap
    if display_heatmap:
        display(sns.heatmap(df.corr(), annot=True, cmap=color_map))
        

        
def show(df: pd.DataFrame, display_columns: list=None, show_count=True,
         subimage_column: str=None, hint: str=None,
         height=DEFAULT_IMAGE_HEIGHT, color_map=DEFAULT_COLOR_MAP,
         ):
    '''
    doc: https://seaborn.pydata.org/generated/seaborn.countplot.html
    col is subgraph label
    
    display category dist
    https://seaborn.pydata.org/generated/seaborn.barplot.html
    cont2cont_action: cont2line or cont2cont
    
    date only be x (can not be y)
    '''
    if display_columns is None:
        display_columns = df.columns 
        
    xy2actions = {
        'is_cont': { 
            'is_cate': None,
            'is_cont': cont2line,
            'is_date': None,
        },
        'is_cat' : {
            'is_cate': cate2cate,
            'is_cont': cate2cont, 
            'is_date': None,
        },
        'is_date' :{
            'is_cont': cont2line,
            'is_cate': None,
            'is_date': None,
        }
    }
    
    
    for i, x_c in enumerate(display_columns):
        for y_c in display_columns[i+1:]:
            print(x_c, y_c)
            x_key = _which_type(df.dtypes[x_c])
            y_key = _which_type(df.dtypes[y_c])
            
            y_action_list = xy2actions[x_key]
            show_image = y_action_list[y_key]
            if show_image is not None:
                display(show_image(df, x_c, y_c, hint=hint, subimage_column=subimage_column, height=height))
            
    if show_count:
        xcount2action = {
            'is_cont': cont2count,
            'is_cate': cate2count,
            'is_date': cont2count,
        }
        for i, x_c in enumerate(display_columns):
            x_key = _which_type(df.dtypes[x_c])
            show_image = xcount2action[x_key]
            display(show_image(df, x_c, hint=hint, subimage_column=subimage_column, height=height))
        
        
def cate2count(df: pd.DataFrame, x, hint=None, subimage_column=None, height=DEFAULT_IMAGE_HEIGHT):
    return sns.catplot(data=df, x=x, 
                       hue=hint, col=subimage_column,
                       kind='count', height=height)

def cont2count(df: pd.DataFrame, x, hint=None, subimage_column=None, height=DEFAULT_IMAGE_HEIGHT):
    d = df[x].value_counts().reset_index()
    y = x + '_count'
    d.rename(columns={'index': x, x: y}, inplace=True)
    return cont2cont(d, x, y, hint=hint, subimage_column=subimage_column, height=height)


def cate2cate(df: pd.DataFrame, x, y, hint=None, subimage_column=None, height=DEFAULT_IMAGE_HEIGHT):
    return sns.catplot(data=df, x=x, y=y, hue=hint, col=subimage_column, height=height)
    

def cate2cont(df: pd.DataFrame, x, y, hint=None, subimage_column=None, height=DEFAULT_IMAGE_HEIGHT):
    return sns.barplot(data=df, x=x, y=y, hue=hint, col=subimage_column, height=height)
    

def cont2line(df: pd.DataFrame, x, y, hint=None, subimage_column=None, height=DEFAULT_IMAGE_HEIGHT):
    '''
    plot trend
    Doc: https://seaborn.pydata.org/generated/seaborn.lineplot.html
    '''
    return sns.lineplot(data=df, x=x, y=y, hue=hint)


def cont2cont(df: pd.DataFrame, x, y, hint=None, subimage_column=None, height=DEFAULT_IMAGE_HEIGHT):
    '''
    x: continuous, y:continuous
    Doc: https://seaborn.pydata.org/generated/seaborn.relplot.html
    '''
    return sns.relplot(data=df, x=x, y=y, hue=hint, col=subimage_column, height=height)


    
def top(df, column: str, n: int=5):
    display(df.sort_values(column, ascending=False).head(n))


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
    elif is_datetime64_any_dtype(dtype):
        return 'is_date'
    else:
        return None
