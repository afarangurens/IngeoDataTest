import pandas as pd
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import io
import base64

# This is to fix a bug on the plotting of the correlation matrix
matplotlib.use('TkAgg')


def read_file(file_path) -> pd.DataFrame:
    """
    Read a file from the specified path and return a pandas DataFrame.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        pandas.DataFrame: The DataFrame containing the data from the file.

    Raises:
        ValueError: If the file type is not supported.
    """
    try:
        df = pd.read_csv(file_path)

        return format_date(df)
    except ValueError as e:
        raise ValueError(f'The type of file isn\'t supported: {e}')


def format_date(df: pd.DataFrame) -> pd.DataFrame:
    """
    Formats the 'Date' column of a Pandas DataFrame to the format 'month-day-year'.

    Args:
        df (pandas.DataFrame): A Pandas DataFrame containing a 'Date' column in the format 'month/day/year'.

    Returns:
        pandas.DataFrame: The input DataFrame with the 'Date' column formatted to the 'month-day-year' format.

    Raises:
        ValueError: If there is an error formatting the 'Date' column.
    """
    try:
        # Reads the Date column, and change the month/day/year format to month-day-year.
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

        # Return the formatted dataframe.
        return df

    except ValueError as e:
        # If an error occurs during the formatting of the Date column, raises the following error.
        raise ValueError(f'There was a problem formating the date, error:{e}')


def get_df_info_by_year(df: pd.DataFrame) -> pd.Series:
    """Return a Pandas Series with the year of each date in the 'Date' column of the input DataFrame.

    Args:
        df (pandas.DataFrame): A Pandas DataFrame containing a 'Date' column.

    Returns:
        pandas.Series: A Pandas Series containing the year of each date in the 'Date' column.
    """
    return df['Date'].dt.year


def get_df_info_by_month(df: pd.DataFrame) -> pd.Series:
    """Return a Pandas Series with the month of each date in the 'Date' column of the input DataFrame.

    Args:
        df (pandas.DataFrame): A Pandas DataFrame containing a 'Date' column.

    Returns:
        pandas.Series: A Pandas Series containing the month of each date in the 'Date' column.
    """
    return df['Date'].dt.month


def time_series_analysis(df: pd.DataFrame, time_frame: str = "year") -> pd.DataFrame:
    """
    Analyzes a time series dataset and returns the mean, variance, and standard deviation
    of the specified time frame. The time frame can be either "year" or "month".

    Args:
        df (pandas.DataFrame): The time series dataset to analyze.
        time_frame (str): The time frame to use for the analysis. Defaults to "year".

    Returns:
        pandas.DataFrame: The mean, variance, and standard deviation of the specified time frame.

    Raises:
        ValueError: If the time frame is not "year" or "month".
    """

    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

    if time_frame.lower() == "year":
        year_data = get_df_info_by_year(df)
        yearly_variance = df.groupby(year_data)["A1"].var()
        yearly_std = df.groupby(year_data)["A1"].std()
        yearly_mean = df.groupby(year_data)["A1"].mean()

        res_df = pd.concat([yearly_mean, yearly_variance, yearly_std], axis=1)
        res_df.columns = ["Mean", "Variance", "Standard Deviation"]
        return res_df

    elif time_frame.lower() == "month":
        month_data = get_df_info_by_month(df)
        month_variance = df.groupby(month_data)["A1"].var()
        month_std = df.groupby(month_data)["A1"].std()
        month_mean = df.groupby(month_data)["A1"].mean()

        res_df = pd.concat([month_mean, month_variance, month_std], axis=1)
        res_df.columns = ["Mean", "Variance", "Standard Deviation"]
        return res_df

    else:
        raise ValueError(f"Time frame for time series analysis must be 'year' or 'month', not {time_frame}.")


def describe_statistically(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates descriptive statistics for the given dataframe.

    Args:
        df (pd.DataFrame): The input dataframe to be described.

    Returns:
        pd.DataFrame: A dataframe containing the descriptive statistics for each column in the input dataframe.

    Raises:
        ValueError: If there was an error calculating the descriptive statistics.
    """

    try:
        # The dataset columns
        categories = ['A1', 'A2', 'A3', 'R1', 'R2', 'R3', 'M1', 'M2', 'M3', 'P1', 'P2', 'P3', 'D1']

        # Set column names for the descriptive dataframe
        res_df = pd.DataFrame(columns=['Category', 'Mean', 'Median', 'Mode', 'Std Dev', 'Variance', 'Min', 'Max'])

        # For each category (column name) calculate the statistics values to describe the data within this column.
        for category in categories:
            mean = df[category].mean()
            median = df[category].median()
            mode = df[category].mode().values[0]
            std_dev = df[category].std()
            variance = df[category].var()
            minimum = df[category].min()
            maximum = df[category].max()

            # Create a row to concatenate it to the dataframe
            row = {
                'Category': category,
                'Mean': mean,
                'Median': median,
                'Mode': mode,
                'Std Dev': std_dev,
                'Variance': variance,
                'Min': minimum,
                'Max': maximum,
            }

            res_df = pd.concat([res_df, pd.DataFrame([row])], ignore_index=True)

        return res_df

    except Exception as e:
        raise ValueError(f"There was an error calculating the central tendencies, error:{e}.")


def gas_diesel_correlation(df: pd.DataFrame, col1: str = 'A1', col2: str = "D1") -> float:
    """
    Computes the Pearson correlation coefficient between the gas and diesel prices in the given dataframe.
    It is a number between -1 and 1, and what this tell us is that if the coefficient between two columns is closer to
    1, that's because there's a strong positive linear correlation between those two columns, if it has a value of -1
    it's because the two columns have a negative linear correlation and if the coefficient is 0 the two columns don't
    correlate at all linearly.

    Parameters:
    df (pandas.DataFrame): A dataframe containing columns for gas and diesel prices.

    Returns:
    float: The Pearson correlation coefficient between gas and diesel prices.
    """
    # Select the columns for gas and diesel prices
    gas_col = df[col1]
    diesel_col = df[col2]

    # Compute the Pearson correlation coefficient
    corr_coef = gas_col.corr(diesel_col, method='pearson')

    return corr_coef


def k_means_clustering(df: pd.DataFrame, n_clusters: int = 10) -> tuple:
    """
    Perform K-Means clustering on the given dataframe.

    Args:
        df (pandas.DataFrame): The data to cluster.
        n_clusters (int): The number of clusters to use.

    Returns:
        tuple: A tuple containing the cluster centers (as a pandas.DataFrame)
            and the labels for each data point (as a numpy.ndarray).
    """
    # Preprocess the data
    # ...
    cluster_data = df[['A1', 'R1', 'M1', 'P1', 'D1']]
    # Create the K-Means model
    kmeans = KMeans(n_clusters=n_clusters, n_init=10)

    # Fit the model to the data
    kmeans.fit(cluster_data)

    # Assign each point to a cluster
    labels = kmeans.labels_

    # Analyze the clusters
    cluster_centers = kmeans.cluster_centers_
    cluster_df = pd.DataFrame(cluster_centers, columns=cluster_data.columns)
    cluster_df['cluster'] = range(n_clusters)

    return cluster_df, labels


def get_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs a correlation analysis on the DataFrame using the Pearson correlation coefficient.

    Args:
        df: Pandas DataFrame containing the variables to be analyzed.

    Returns:
        corr_df: Pandas DataFrame containing the Pearson correlation coefficient between all pairs of variables.
    """
    # Calculate the correlation coefficients using the Pearson method
    corr_df = df.corr(method='pearson', numeric_only=True)

    return corr_df


def plot_correlation_matrix(df):
    """
       Plot the correlation matrix of a given dataframe.

       Args:
           df (pandas.DataFrame): The data to plot.

       Returns:
           None.
    """

    df_corr = get_correlation_matrix(df)
    sns.heatmap(df_corr, cmap='coolwarm', annot=True, fmt='.2f',
                square=True, linewidths=.5, cbar_kws={"shrink": .5})

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return graphic



