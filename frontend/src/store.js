import { createStore } from 'redux';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';

const reducer = (state = {userType: ''}, action) => {
  console.log('executing action')
  switch (action.type){
    case 'CINEMAMANAGER':
      return {
        userType: 'CINEMAMANAGER'
      }
    case 'STUDENT':
      return {
        userType: 'STUDENT'
      }
    case 'GUEST':
      return {
        userType: 'GUEST'
      }
    case 'ACCOUNTMANAGER':
      return {
        userType: 'ACCOUNTMANAGER'
      }
      case 'CLUBREP':
      return {
        userType: 'CLUBREP'
      }
    default: 
    console.log('default')
      return state
  }

};

const persistConfig = {
  key: 'root',
  storage
}

const persistedReducer = persistReducer(persistConfig, reducer);

export const store = createStore(persistedReducer);

export const persistor = persistStore(store);

export default store