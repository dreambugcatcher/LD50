from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from pickle import load
from sklearn.metrics import r2_score, root_mean_squared_error


with open('data/calc_data.pickle', 'rb') as file:
    arr_X, arr_Y = load(file)

x_train, x_test, y_train, y_test = train_test_split(
    arr_X, arr_Y, test_size=0.2, random_state=42)

rf = RandomForestRegressor()
pg = {'n_estimators': [50, 100, 150, 200, 250]}
reg_forest = RandomForestRegressor(max_depth=2).fit(x_train, y_train.ravel())
y_pred = reg_forest.predict(x_test)
print(r2_score(y_test, y_pred), root_mean_squared_error(y_test, y_pred))
print(f'Forest: R^2 = {reg_forest.score(x_test, y_test):.3f}')
