class model():

    def __init__(self):
        self.layers = []
        

    def normalization(self,Arr):
      epsilon=0.0000001
      arr=0 
      arr = Arr - Arr.mean(axis=0)
      arr = arr / (np.abs(arr).max(axis=0)+epsilon)
      return arr

    def add(self,Layer):
      self.layers.append(Layer)  

    def summary(self):
      # Initializing a table
      sum=0
      table = Texttable()
      table.header(["Layer", "filters size", "number of filters", "pad", "stride", "number of paramters"])
      for layer in self.layers:
        if type(layer)==Conv:
          F=layer.f
          numLayers=layer.n_C
          K=layer.n_C_prev
          parameters=(F*F*K+1)*numLayers
          sum+=parameters
          table.add_row(["Conv layer", "{}x{}".format(F,F),numLayers ,layer.padding,layer.stride,parameters])
        elif type(layer)==Dense:
          sum+=layer.biases.size+layer.weights.size
          table.add_row(["Dense layer","-","-" ,"-","-",layer.biases.size+layer.weights.size])
        elif type(layer)==Pool:
          F=layer.f
          table.add_row(["Pool layer", "{}x{}".format(F,F),"-" ,layer.padding,layer.stride,"0"])
        else:
          table.add_row(["flatten layer", "-","-" ,"-","-","0"])
      table.add_row(["Total", "-","-" ,"-","-",sum])
      print(table.draw())

    def evaluate(self, x_test , y_test, loss_type="categorical_crossentropy", batchsize=1,metrics="accuracy"):
          lossobj=Loss(loss_type)
          evaluationobj=Evaluation_metrics(metrics,max(y_test),plot)
          output_layer=[]
          forward_outputs=[]
          test_predection=[]
          flatten_shape=0
          #samples=len(x_test)
          samples=100
          batches=int(samples/batchsize)
          print("Testing is running----------------->")
          new_samples=len(x_test)
          test_predection.clear()
          forward_outputs.clear()
          for j in range(batches):       
            for b in range(batchsize):    
              output_layer.clear()     
              forward_input=0    
              forward_input = x_test[j*batchsize+b]
              data=forward_input
              output_layer.append(data)
              # forward propagation       
              for layer in self.layers:
                  if (layer=="flatten"):
                    flatten_shape=forward_input.shape                      
                    forward_input=forward_input.flatten()
                    output_layer.append(forward_input)                                          
                  else:    
                    forward_input = layer.forward(forward_input)
                    output_layer.append(forward_input) 
              forward_outputs.append(np.argmax(output_layer[-1]))
              test_predection.append(output_layer[-1])     
          
          print("Loss ={}     ".format(lossobj.loss (test_predection, y_test[0:samples])))
          if (metrics!="confusion matrix"):
            print(evaluationobj.all_evaluation(forward_outputs,y_test[0:samples]))
          else :
            evaluationobj.all_evaluation(forward_outputs,y_test[0:samples])  

    def fit(self, x_train, y_train, loss_type="categorical_crossentropy" ,epochs=0, validation_split=0.1,batchsize=1,plot=1,metrics="accuracy"):
        lossobj=Loss(loss_type)
        evaluationobj=Evaluation_metrics(metrics,max(y_train),plot)
        Visualizerobj=Visualizer(metrics)
        Visualizerobj_validate=Visualizer(metrics)

        datalength = len(x_train)
        splitor=int(datalength*validation_split)
        x_validation = x_train[0:splitor]  #as i get the data randamly so i always get from the beggining to the disered length
        y_validation = y_train[0:splitor]
        x_train =      x_train[splitor:]
        y_train =      y_train[splitor:]
        state=np.random.get_state()
        np.random.shuffle(x_validation)
        np.random.set_state(state)
        np.random.shuffle(y_validation)
        output_layer=[]
        output_batch_layer=[]
        batch_grad=[]
        forward_outputs=[]
        validation_forward_outputs=[]
        train_predection=[]
        validation_predection=[]
        flatten_shape=0
        #samples= 200
        #validation_samples=300
        samples= len(x_train)
        validation_samples=len(x_validation)
        batches=int(samples/batchsize)
        for i in range(epochs):

            #shuffling
            state=np.random.get_state()
            np.random.shuffle(x_train)
            np.random.set_state(state)
            np.random.shuffle(y_train)

            new_samples=len(x_train)
            validation_grad=0
            train_predection.clear()
            validation_predection.clear()
            validation_forward_outputs.clear()
            forward_outputs.clear()
  
            for j in range(batches):

              output_batch_layer.clear()
              batch_grad.clear()

              for b in range(batchsize):    

                output_layer.clear()     
                forward_input=0    
                forward_input = x_train[j*batchsize+b]
                data=forward_input
                output_layer.append(data)
                # forward propagation       

                for layer in self.layers:

                    if (layer=="flatten"):
                      flatten_shape=forward_input.shape                      
                      forward_input=forward_input.flatten()
                      output_layer.append(forward_input)                                          
                    else:    
                      #if (type(layer) == Conv or Dense ):
                        #norm=np.linalg.norm(forward_input)
                        #forward_input=forward_input/(norm+0.00000001)
                      forward_input = layer.forward(forward_input)
                      output_layer.append(forward_input)
                          
                forward_outputs.append(np.argmax(output_layer[-1]))
                train_predection.append(output_layer[-1])
                grad=lossobj.delta_loss(output_layer[-1],y_train[j*batchsize+b])
                output_batch_layer.append(output_layer)
                batch_grad.append(grad)
                #backward propagation  
              reversed_layers= self.layers[::-1]
              
              for k in range(batchsize):
                back=len(output_batch_layer[k])-2    
                for rlayer in  reversed_layers: 
                    if (rlayer=="flatten"):
                      backward_output=backward_output.reshape(flatten_shape)   
                      batch_grad[k]=backward_output   
                      back=back-1
                    else:
                      backward_output=rlayer.backward(batch_grad[k],output_batch_layer[k][back])
                      batch_grad[k]=backward_output
                      back=back-1

            #print("validation is running----------------->")
            for l in range(validation_samples):  
                validation_forward_input= x_validation[l]
                for layer in self.layers:
                  if (layer=="flatten"):            
                      validation_forward_input=validation_forward_input.flatten()           
                  else:
                      validation_forward_input= layer.forward(validation_forward_input)       
                validation_forward_outputs.append(np.argmax(validation_forward_input))
                validation_predection.append(validation_forward_input)
        

            if plot:
              if metrics=="all":
                precision,recall,F1,accuracy=evaluationobj.all_evaluation(forward_outputs,y_train)  
                log={    
                    "type": "train",   
                    "loss":lossobj.loss (train_predection, y_train),
                    "accuracy" :accuracy,
                    "precision":precision,
                    "f1":F1,
                    "recall":recall
                }
              else:
                log={         
                    "type": "train"  ,           
                    "loss" : lossobj.loss (train_predection, y_train),
                    metrics : evaluationobj.all_evaluation(forward_outputs,y_train)  
                }           
              if (metrics!="confusion matrix"):
                Visualizerobj.on_epoch_end(log)
              else :
                evaluationobj.all_evaluation(forward_outputs,y_train)  


              if metrics=="all":
                precision,recall,F1,accuracy=evaluationobj.all_evaluation(validation_forward_outputs,y_validation)  
                log={ 
                    "type": "test" ,                               
                    "loss":lossobj.loss (validation_predection, y_validation),
                    "accuracy" :accuracy,
                    "precision":precision,
                    "f1":F1,
                    "recall":recall
                }
              else:
                log={   
                    "type": "test" ,                            
                    "loss" : lossobj.loss (validation_predection, y_validation),
                    metrics : evaluationobj.all_evaluation(validation_forward_outputs,y_validation)  
                }           
              if (metrics!="confusion matrix"):
                Visualizerobj_validate.on_epoch_end(log)
              else :
                evaluationobj.all_evaluation(validation_forward_outputs,y_validation)  


            else:
              print("Epoch {}--------------------->".format(i+1))
              print("Training_Loss = {}".format(lossobj.loss (train_predection, y_train)))
              if (metrics!="confusion matrix"):
                if metrics=="all":
                  p,r,f1,a=evaluationobj.all_evaluation(forward_outputs,y_train)
                  print("Percision= {:.2f} ,Recall={:.2f},F1Score= {:.2f} ,Accuracy= {:.2f} ".format(p,r,f1,a))
                else:
                  print("{} = {:.2f}  ".format( metrics ,evaluationobj.all_evaluation(forward_outputs,y_train)))
              else :
                print("confusion matrix")
                evaluationobj.all_evaluation(forward_outputs,y_train)
              print("==============================================================================================================")
              print("validation_loss = {}".format( lossobj.loss (validation_predection, y_validation)))
              if (metrics!="confusion matrix"):
                if metrics=="all":
                  p,r,f1,a=evaluationobj.all_evaluation(validation_forward_outputs,y_validation)
                  print("Percision= {:.2f} ,Recall={:.2f},F1Score= {:.2f} ,Accuracy= {:.2f} ".format(p,r,f1,a))
                else:
                  print("{} = {:.2f}  ".format( metrics ,evaluationobj.all_evaluation(validation_forward_outputs,y_validation)))
              else :
                print("confusion matrix")
                evaluationobj.all_evaluation(validation_forward_outputs,y_validation)
              print("==============================================================================================================")
