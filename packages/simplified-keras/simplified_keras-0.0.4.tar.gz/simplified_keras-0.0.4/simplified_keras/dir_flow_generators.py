from keras.preprocessing.image import ImageDataGenerator
import os


# tran data has to be in train folder and validation data has to be in val folder
def get_train_val_generators(img_datagen: ImageDataGenerator, data_dir='../data', color_mode='rgb',
                             batch_size=128, class_mode='categorical', **kwargs):
    train_generator = img_datagen.flow_from_directory(os.path.join(data_dir, 'train'),
                                                      batch_size=batch_size,
                                                      color_mode=color_mode,
                                                      class_mode=class_mode,
                                                      **kwargs)
    validation_generator = img_datagen.flow_from_directory(os.path.join(data_dir, 'val'),
                                                           batch_size=batch_size,
                                                           color_mode=color_mode,
                                                           class_mode=class_mode,
                                                           **kwargs)
    return train_generator, validation_generator
