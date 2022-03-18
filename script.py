import pandas as pd
import numpy as np

def random_dates(start = pd.to_datetime('2022-01-01'), end = pd.to_datetime('2022-01-5'), sample_size = 100, unit='D', seed=None):
    """
    start - Date from generation starts
    end - Date where generation stop
    sample_size
    unit - Denotes the unit of the arg for numeric
    seed - random seed

     return array of Timestamp
    """
    if not seed:
        np.random.seed(0)

    ndays = (end - start).days + 1
    return start + pd.to_timedelta(
        np.random.randint(0, ndays, size=sample_size), unit=unit
    )


def generate_data(size=1000, unique_users=50):
    """
    size - size of DataFrame
    unique_users - number of unique users

    return DataFrame
    """

    values = {'date': random_dates(sample_size = size),
              'user_id': np.random.randint(unique_users, size=size),
              'operation_name': np.random.choice(['call', 'traffic', 'sms'], size=size),
              'value_spent': np.random.randint(100, size=size)
              }

    data = pd.DataFrame(values)
    data = data.sort_values(by=['user_id']).reset_index(drop=True)

    return data


def make_pivot_table(data):
    """
    data - input DataFrame to Transform

    return grouped by day and user_id, services
    """

    output = pd.pivot_table(data, values='value_spent', index=['user_id', 'date'], columns='operation_name',
                            aggfunc=np.sum, fill_value=0)
    output.reset_index(inplace=True)
    output = pd.DataFrame(output.values, columns=list(output.columns))

    return output

data = generate_data(size=100000, unique_users=1000)
output = make_pivot_table(data)
print(output.head(20))
