# TODO list

- [x]   add old list parsing into makeList.py
- [x] modify makeList to accept arguments
- [x ]   verify operation in binary (rts/non-rts) mode
- [ ]   verify operation in categorical mode
- [x ] add flags in Settings.py to allow the makeDataSets to change how the model is fit
          i.e. the switch between 'binary_crossentropy' and 'categorical_crossentropy'
- [ ] Change testing data to old dataset for now
- [ ] split model training into primary (rts/nrts) and secondary ({m,e,g}rts/nrts) models
- [ ] in orignal version verify if categorical accuracy is as high as binary via the code snippet
Code snippit:
```python
from keras.metrics import categorical_accuracy
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=[categorical_accuracy])
```
- [ ] Update the main todo list by the list below:
https://gist.github.com/gravetaxon/67c2891f5d665f07589fae576b802ee6

- [ ] Verify that the output DENSE function is of the correct for multi-class operations.
- [ ] https://machinelearningmastery.com/multi-class-classification-tutorial-keras-deep-learning-library/

RE: Meeting May 9th:
- [ ] Add amplitude calculations for a graph
- [ ] Train multiple models: N v N, R v N, M v N, E v N 
   + [ ] Compare output relative to actual graphs
   + [ ] Use voter model to ident which of the categories match best
   + [ ] For RTS-Ident graphs use amp calc to determine the quantity of specific amplitutde ranges


