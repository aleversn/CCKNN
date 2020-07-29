# %%
from CCKNN.predict import Predicter

predicter = Predicter('./train.csv', True)
predicter.pred([3,2])

# %%
