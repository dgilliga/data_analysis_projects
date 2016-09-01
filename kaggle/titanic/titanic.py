import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas import Series
import statsmodels.api as sm
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier


# This function was intended to create a reduced model with the minimum scoring aic values.
# It uses sm.OLS which is for regression only so was only useful If i use Y as a continuous varaible
def myAIC(y, X):
    # so basically we start creating our overall dataframe with the constant as the first value
    overall_df = DataFrame(X['ones'])
    overall_mod = sm.OLS(y, overall_df)
    overall_res = overall_mod.fit()
    print overall_res.summary()

    X_no_ones = X.drop(['ones'], axis=1)
    count = 0

    min_col = 'start'
    # we will have at most 100 features or break the loop if the aic is not getting smaller.
    while count < 100 and min_col != 'None':
        count += 1
        min_aic = overall_res.aic
        min_col = 'None'
        for column in X_no_ones.columns:
            cur_df = overall_df.copy()
            cur_df[column] = X_no_ones[column]
            cur_mod = sm.OLS(y, cur_df)
            cur_res = cur_mod.fit()
            if cur_res.aic < overall_res.aic and cur_res.aic < min_aic:
                min_aic = cur_res.aic
                min_col = column

        # if we have found a new min then let's update our full model and cut the column from the predictor values.
        if min_col != 'None':
            overall_df[min_col] = X_no_ones[min_col]
            overall_mod = sm.Logit(y, overall_df)
            overall_res = overall_mod.fit()
            X_no_ones = X.drop([i for i in overall_df.columns], axis=1)

    return overall_df


# EXTRACT import raw training and test sets
test_raw = pd.read_csv("/Users/darrengilligan1/Documents/edu/advancedmachinelearning/titanic/test.csv",
                       dtype={"Age": np.float64}, )
training_raw = pd.read_csv(
    "/Users/darrengilligan1/Documents/edu/advancedmachinelearning/titanic/copy_of_the_training_data.csv",
    dtype={"Age": np.float64}, )

# TRANSFORM

training = training_raw.copy()
test = test_raw.copy()

# impute the age where missing with mean age
age = training.Age
imputed_na_age = age.fillna(round(age.dropna().mean(), 2))
training.Age = imputed_na_age

# impute the test data age where missing with mean age
test_age = test.Age
imputed_test_na_age = test_age.fillna(round(test_age.dropna().mean(), 2))
test.Age = imputed_test_na_age

# impute the missing for Embarked value with most frequent value for Embarked ===> NOT A GOOD METHOD
training.Embarked = training.Embarked.fillna(training.Embarked.value_counts().index[0])

# Delete features which are all unique (subjective)

for i in ['Cabin', 'Ticket', 'Name', 'PassengerId']:
    training = training.drop(i, 1)
    test = test.drop(i, 1)
# get response variable and delete from training data
y = training_raw.Survived
X = training.drop('Survived', 1)

# forest_X = X.copy()
#
# forest = forest_X.Embarked.map(lambda x: {'Q':1,'S':2,'C':3})

for i in ['Embarked', 'Pclass', 'Sex']:
    test = test.join(pd.get_dummies(test[i], prefix=i))
    test = test.drop(i, 1)
    X = X.join(pd.get_dummies(X[i], prefix=i))
    X = X.drop(i, 1)



# rf_fit = RandomForestClassifier(n_estimators=5, random_state=123).fit(X, y)


for i in ['Embarked', 'Pclass', 'Sex']:
    test = test.join(pd.get_dummies(test[i], prefix=i))
    test = test.drop(i, 1)
    X = X.join(pd.get_dummies(X[i], prefix=i))
    X = X.drop(i, 1)

total_columns = [np.NaN] * 100

for i in range(100):
    X_train = X.copy()
    y_train = y.copy()
    # X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=i)
    X_train['ones'] = np.ones(len(X_train.Age))
    overall_df = myAIC(y_train, X_train)
    total_columns[i] = overall_df.columns

total_columns = Series(total_columns)


# X_train = X_train.drop('ones', 1)
# overall_df= overall_df.drop('ones',1)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=i)

X_train = DataFrame(overall_df.ix[X_train.index])
X_test = DataFrame(overall_df.ix[X_test.index])

X_train.index = range(len(X_train.index))
X_test.index = range(len(X_test.index))
y_train.index = range(len(y_train.index))
y_test.index = range(len(y_test.index))

# rf_vals = range(5, 35, 5)
# rf_scores = [RandomForestClassifier(n_estimators=rf_val, random_state=123).fit(X_train, y_train).score(X_test, y_test)
#              for rf_val in rf_vals]
#
X_final_test = DataFrame()
X_final_test['ones']= np.ones(len(test['Sex_female']))
for i in X_train.columns.drop('ones'):
    X_final_test[i] = test[i]

# rf_fit = RandomForestClassifier(n_estimators=5, random_state=123).fit(X_train, y_train)



sm_fit = sm.Logit(y_train, X_train).fit()

sm_fit.predict(X_final_test)

d = {'PassengerId': test_raw.PassengerId, 'Survived': (sm_fit.predict(X_final_test)> 0.5).astype(int)}
final_result = DataFrame(d)


csv = final_result.to_csv(index=False)