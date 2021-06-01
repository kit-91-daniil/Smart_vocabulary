from datetime import datetime
from flask_security import UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

roles_users = db.Table("roles_users",
                       db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
                       db.Column("role_id", db.Integer(), db.ForeignKey("role.id"))
                       )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean())
    words = db.relationship("Words", back_populates="user", lazy="dynamic",
                            cascade="all, delete-orphan")
    interval_words = db.relationship("IntervalWords", back_populates="user",
                                     lazy="dynamic", cascade="all, delete-orphan"
                                     )
    learned_words = db.relationship("LearnedWords", back_populates="user",
                                    lazy="dynamic", cascade="all, delete-orphan")
    phrasal_verbs = db.relationship("PhrasalVerbs", back_populates="user",
                                    lazy="dynamic", cascade="all, delete-orphan")
    interval_phrasal_verbs = db.relationship("IntervalPhrasalVerbs", back_populates="user",
                                             lazy="dynamic", cascade="all, delete-orphan")
    learned_phrasal_verbs = db.relationship("LearnedPhrasalVerbs", back_populates="user",
                                            lazy="dynamic", cascade="all, delete-orphan")
    roles = db.relationship("Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")
                            )

    def __repr__(self):
        return f"email: {self.email}"


class PhrasalVerbsVocabulary(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    phrasal_verb = db.Column(db.String(60), nullable=False)
    translation = db.Column(db.String(60), nullable=False)
    key_word = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(120))
    example = db.Column(db.String(120))
    users = db.relationship("PhrasalVerbs", back_populates="vocabulary",
                            lazy="dynamic", cascade="all, delete-orphan")
    interval_users = db.relationship("IntervalPhrasalVerbs", back_populates="vocabulary",
                                     lazy="dynamic", cascade="all, delete-orphan")
    learned_users = db.relationship("LearnedPhrasalVerbs", back_populates="vocabulary",
                                    lazy="dynamic", cascade="all, delete-orphan")
    __table_args__ = (db.UniqueConstraint("phrasal_verb", "translation", name="unique_phrasal_verb_translation"),)


class LearnedPhrasalVerbs(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey("phrasal_verbs_vocabulary.id"), primary_key=True)
    addition_time = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    user = db.relationship("User", back_populates="learned_phrasal_verbs")
    vocabulary = db.relationship("PhrasalVerbsVocabulary", back_populates="learned_users")

    def __repr__(self):
        return f"User id: {self.user_id}, word id:  {self.word_id}"


class PhrasalVerbs(db.Model):
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), primary_key=True)
    word_id = db.Column(db.Integer(), db.ForeignKey("phrasal_verbs_vocabulary.id"), primary_key=True)
    addition_time = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    user = db.relationship("User", back_populates="phrasal_verbs")
    vocabulary = db.relationship("PhrasalVerbsVocabulary", back_populates="users")

    def __repr__(self):
        return f"User id: {self.user_id}, word id:  {self.word_id}"


class IntervalPhrasalVerbs(db.Model):
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), primary_key=True)
    word_id = db.Column(db.Integer(), db.ForeignKey("phrasal_verbs_vocabulary.id"), primary_key=True)
    addition_time = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    repeating_time = db.Column(db.DateTime)
    time_to_repeat = db.Column(db.Integer)
    status = db.Column(db.Integer, default=1)
    user = db.relationship("User", back_populates="interval_phrasal_verbs")
    vocabulary = db.relationship("PhrasalVerbsVocabulary", back_populates="interval_users")

    def __repr__(self):
        return f"User id: {self.user_id}, word id:  {self.word_id}, " \
               f"addition_time: {self.addition_time}, " \
               f"repeating_time: {self.repeating_time}, " \
               f"time to repeat: {self.time_to_repeat}, " \
               f"status: {self.status}"


class Vocabulary(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    word = db.Column(db.String(40))
    translation = db.Column(db.String(40), nullable=False)
    interval_users = db.relationship("IntervalWords", back_populates="vocabulary",
                                     lazy="dynamic", cascade="all, delete-orphan")
    users = db.relationship("Words", back_populates="vocabulary",
                            lazy="dynamic", cascade="all, delete-orphan")
    learned_users = db.relationship("LearnedWords", back_populates="vocabulary",
                                    lazy="dynamic", cascade="all, delete-orphan")
    __table_args__ = (db.UniqueConstraint("word", "translation", name="unique_word_translation"),)

    def __repr__(self):
        return f"{self.word} - {self.translation}"


class Words(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey("vocabulary.id"), primary_key=True)
    addition_time = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    user = db.relationship("User", back_populates="words")
    vocabulary = db.relationship("Vocabulary", back_populates="users")

    def __repr__(self):
        return f"User id: {self.user_id}, word id:  {self.word_id}"


class IntervalWords(db.Model):
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), primary_key=True)
    word_id = db.Column(db.Integer(), db.ForeignKey("vocabulary.id"), primary_key=True)
    addition_time = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    repeating_time = db.Column(db.DateTime)
    time_to_repeat = db.Column(db.Integer)
    status = db.Column(db.Integer, default=1)
    user = db.relationship("User", back_populates="interval_words")
    vocabulary = db.relationship("Vocabulary", back_populates="interval_users")

    def __repr__(self):
        return f"User id: {self.user_id}, word id:  {self.word_id}, " \
               f"addition_time: {self.addition_time}, " \
               f"repeating_time: {self.repeating_time}, " \
               f"time to repeat: {self.time_to_repeat}, " \
               f"status: {self.status}"


class LearnedWords(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey("vocabulary.id"), primary_key=True)
    addition_time = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    user = db.relationship("User", back_populates="learned_words")
    vocabulary = db.relationship("Vocabulary", back_populates="learned_users")

    def __repr__(self):
        return f"User id: {self.user_id}, word id:  {self.word_id}"


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f"role: {self.name}, description: {self.description}"


if __name__ == "__main__":
    pass
    # db.drop_all()
    # db.create_all()
    """Первое добавление пользователя, слова и ассоциации"""
    # u1 = User(login="login1", name="name1")
    # voc1 = Vocabulary(word="word1")
    # word = Words()
    # word_ = Words(user=u1, vocabulary=voc1)
    # db.session.add_all([u1, voc1])
    """Добавление слова и ассоциации"""
    # user1 = User.query.filter(User.name == 'name1').first()
    # voc2 = Vocabulary(word="word2")
    # word2 = Words(user=user1, vocabulary=voc2)
    # db.session.add(voc2)
    # db.session.commit()
    """добавление ассоциации"""
    # user1 = User.query.filter(User.name == 'name1').first()
    # voc3 = Vocabulary.query.filter(Vocabulary.word == "word2").first()
    # word3 = Words(user=user1, vocabulary=voc3)
    # db.session.add(word3)
    # db.session.commit()

    # user1 = User.query.filter(User.name == 'name1').first()
    # user2 = User(name='name2', login="login2")
    # voc5 = Vocabulary(word="word5")
    # word4 = Words(user=user2, vocabulary=voc5)
    # db.session.add(voc5)
    # db.session.commit()
