# def filter_by_index(data: np.ndarray, index_to_delete):
#     """

    # Parameters
    # ----------
    # data: data to filter
    # index_to_delete: an array of index to be deleted

    # Returns
    # -------
    # filtered data
    # """
    # target_data = data
    # index_to_delete = list(set(index_to_delete))  # make sure index_to_delete is a set(unique values)
    # filtered_data = []
    # for column in target_data:
    #     new_column = np.delete(column, index_to_delete)
    #     filtered_data.append(new_column)
    #
    # filtered_data = np.array(filtered_data, dtype='float32')
    #
    # return filtered_data


def filter_outliers(self, column_to_filter: int):
    data_to_filter = self.data_to_fit[column_to_filter]
    mean = np.mean(data_to_filter)
    std = np.std(data_to_filter)
    outlier_index = []
    abs(data_to_filter[index] - mean) < 2 * std
    for index in range(len(data_to_filter)):
        if abs(data_to_filter[index] - mean) < 2 * std:
            outlier_index.append(index)

    refined_data = filter_by_index(self.data_to_fit, outlier_index)
#
    self.data_to_fit = refined_data

# def try_plot(self, x_label, y_label, title):
#     plt.figure()
#     plt.plot(self.data[0], self.data[1], 'ro', markersize=0.5)

# plt.xlabel(x_label)
# plt.ylabel(y_label)
# plt.title(t/itle)
# plt.savefig(f'plots/{title}.png', dpi=600)

# def check_dimension(self):
#     dimension = len(self.data)
#     for column_index in range(dimension):
#         for further_index in range(column_index + 1, dimension):
#             if len(self.data[column_index]) != len(self.data[further_index]):
#                 raise ValueError(f"Column {column_index} and Column {further_index} must have the same dimension\n"
#                                  f"dim Column {column_index} = {len(self.data[column_index])}"
#                                  f"dim Column {further_index} = {len((self.data[further_index]))}")


class MinimumOf:
    def __init__(self, data_input: pd.DataFrame, fitting_model, x_column=0, y_column=1):
        # attributes
        # target data and model
        self.df = data_input
        self.x = self.df.iloc[:, x_column]
        self.y = self.df.iloc[:, y_column]
        self.model = fitting_model
        # fitting parameters
        self.params = None
        self.cov = None
        # prediction
        self.predicted_y = None
        self.minimum = []
        # methods
        self.find_minimum()

    def find_minimum(self, value_range=None, column_to_crop=0, err_column=2):
        pass
        if value_range:
            lower_bound, upper_bound = value_range
            mask = (self.df.iloc[:, column_to_crop] >= lower_bound) & (self.df.iloc[:, column_to_crop] <= upper_bound)
            self.df = self.df[mask]

        if self.df.shape[1] == 3:
            err = self.df.iloc[:, err_column]
            self.params, self.cov = curve_fit(self.model, self.x, self.y, sigma=err)

        if self.df.shape[1] == 2:
            self.params, self.cov = curve_fit(self.model, self.x, self.y)

        self.predicted_y = self.model(self.x, *self.params)
        index_of_min = self.predicted_y.idxmin()

        # Use the index to retrieve the corresponding value from 'x'
        self.minimum = [self.x.loc[index_of_min], self.y.loc[index_of_min]]

    def plot(self, title, save_as, x_label='x', y_label='y'):

        plt.figure()
        plt.plot(self.x, self.y, 'ro', markersize=0.5)
        plt.plot(self.x, self.predicted_y)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(f'minimum finding of {title}')
        plt.savefig(f'plots/{save_as}.png')
        plt.clf()

    def filter_rogue_err(self, err_column_number=2):
        """
        Delete data points where the error is invalid.
        """
        self.data = self.data[self.data.iloc[:, err_column_number] > 0]