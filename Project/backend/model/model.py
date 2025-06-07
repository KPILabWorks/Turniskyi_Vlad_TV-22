import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Flatten, Dense, Concatenate, Dropout, Lambda, GlobalAveragePooling1D


class DotaMatchPredictor:
    def __init__(self, num_heroes=146, embedding_dim=16):
        self.num_heroes = num_heroes
        self.embedding_dim = embedding_dim
        self.model = self._build_model()

    def _build_model(self):
        radiant_input = Input(shape=(5,), name='radiant_heroes')
        dire_input = Input(shape=(5,), name='dire_heroes')
        rank_input = Input(shape=(1,), name='rank')

        hero_embedding = Embedding(self.num_heroes, self.embedding_dim, name='hero_embedding')
        

        radiant_emb = GlobalAveragePooling1D()(hero_embedding(radiant_input))
        dire_emb = GlobalAveragePooling1D()(hero_embedding(dire_input))

        x = Concatenate()([radiant_emb, dire_emb, rank_input])
        x = Dense(64, activation='relu')(x)
        x = Dropout(0.3)(x)
        x = Dense(32, activation='relu')(x)
        output = Dense(1, activation='sigmoid')(x)

        model = Model(inputs=[radiant_input, dire_input, rank_input], outputs=output)
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def fit(self, radiant_ids, dire_ids, ranks, y, batch_size=256, epochs=10, validation_split=0.2):
        self.model.fit(
            {'radiant_heroes': radiant_ids, 'dire_heroes': dire_ids, 'rank': ranks},
            y,
            batch_size=batch_size,
            epochs=epochs,
            validation_split=validation_split
        )

    def predict(self, radiant_ids, dire_ids, ranks):
        return self.model.predict({'radiant_heroes': radiant_ids, 'dire_heroes': dire_ids, 'rank': ranks})

    def save(self, path):
        self.model.save(path)

    def load(self, path):
        self.model = tf.keras.models.load_model(path)



