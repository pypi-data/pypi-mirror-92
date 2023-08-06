import keras.callbacks as clb


def get_default_callbacks(model_name):
    return [
        clb.ReduceLROnPlateau(monitor='val_acc', factor=0.5, min_lr=1e-6, patience=3, verbose=1),
        clb.EarlyStopping(monitor='val_acc', patience=7, verbose=1),
        clb.ModelCheckpoint(monitor='val_acc', filepath=f'../models/{model_name}.h5',
                            save_best_only=True, verbose=1)
    ]
