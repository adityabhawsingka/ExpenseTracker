from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, func, Boolean, Float, desc, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from datetime import datetime
from kivy.properties import ObjectProperty

Base = declarative_base()
Session = ObjectProperty()


def init_session(f_path):
    global Session
    engine = create_engine(f"sqlite:///{f_path}")
    Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class Items(Base):
    """Base user class"""
    __tablename__ = "items"
    item_id = Column(Integer,primary_key=True)
    item_name = Column(String)
    item_link = Column(Integer)
    active = Column(Boolean)

    def __init__(self, **kwargs):
        self.item_id = kwargs['item_id']
        self.item_name = kwargs['item_name']
        self.item_link = kwargs['item_link']
        self.active = kwargs['active']

    def get_item(**kwargs):
        item_name = kwargs['item_name']
        item_link = kwargs['item_link']
        item_id = None
        with session_scope() as session:
            if item_link is None:
                item = session.query(Items).filter(Items.item_name == item_name).first()
            else:
                item = session.query(Items)\
                    .filter(Items.item_name == item_name, Items.item_link == item_link).first()
            if item is not None:
                item_id = item.item_id
        return item_id

    def get_all_items():
        with session_scope() as session:
            items = session.query(Items).order_by(Items.item_name).all()
            item_dict = {}
            for item in items:
                item_dict[item.item_id] = {'item_name': item.item_name,
                                           'item_link': item.item_link,
                                           'active': item.active}
        return item_dict

    def get_items(**kwargs):
        item_name = kwargs['item_name']
        item_type = kwargs['item_type']
        with session_scope() as session:
            if item_type == 'main':
                items = session.query(Items).filter(Items.item_link == 0
                                                    , Items.item_name.like('%{}%'.format(item_name)))\
                    .order_by(Items.item_name).all()
            elif item_type == 'sub':
                items = session.query(Items).filter(Items.item_link != 0
                                                    , Items.item_name.like('%{}%'.format(item_name)))\
                    .order_by(Items.item_name).all()
            elif item_type == 'all':
                items = session.query(Items).filter(Items.item_name.like('%{}%'.format(item_name)))\
                    .order_by(Items.item_name).all()

            item_dict = {}
            for item in items:
                item_dict[item.item_id] = {'item_name': item.item_name,
                                           'item_link': item.item_link,
                                           'active': item.active}
        return item_dict

    def get_items_by_link(**kwargs):
        item_link = kwargs['item_link']
        with session_scope() as session:
            items = session.query(Items).filter(Items.item_link == item_link)\
                .order_by(Items.item_name).all()
            item_dict = {}
            for item in items:
                item_dict[item.item_id] = {'item_name': item.item_name,
                                           'item_link': item.item_link,
                                           'active': item.active}
        return item_dict

    def get_main_items():
        with session_scope() as session:
            items = session.query(Items).filter(Items.item_link == 0).order_by(Items.item_name).all()
            item_dict = {}
            for item in items:
                item_dict[item.item_id] = {'item_name': item.item_name,
                                           'item_link': item.item_link,
                                           'active': item.active}

        return item_dict

    def update_active(**kwargs):
        item_id = kwargs['item_id']
        active = kwargs['active']
        with session_scope() as session:
            item = session.query(Items).filter(Items.item_id == item_id).first()
            if item.item_link == 0:
                session.query(Items).filter(Items.item_id == item_id).update({'active': active})
                session.query(Items).filter(Items.item_link == item_id).update({'active': active})
                return 'refresh'
            else:
                main_item = session.query(Items).filter(Items.item_id == item.item_link).first()
                if main_item.active == False:
                    return 'revert'
                else:
                    session.query(Items).filter(Items.item_id == item_id).update({'active': active})
                    return ''

    def add_item(**kwargs):
        with session_scope() as session:
            item = Items(**kwargs)
            session.add(item)

    def get_next_item_id():
        with session_scope() as session:
            item_id = session.query(func.max(Items.item_id)).one()[0]
        if item_id is None:
            item_id = 1
        else:
            item_id = item_id + 1
        return item_id

    def data_correction():
        with session_scope() as session:
            session.query(Items).filter(Items.item_id == 22).update({'item_link': 0})
            session.query(Items).filter(Items.item_id == 28).update({'item_name': 'Bus'})
            session.query(Items).filter(Items.item_id == 29).update({'item_name': 'Train'})
            item = session.query(Items.item_id).filter(Items.item_link == 25, Items.item_name == 'Flight').first()

            if item is None:
                item_id = Items.get_next_item_id()
                session.add(Items(item_id=item_id, item_name='Flight', item_link=25, active=1))
            session.query(Items).filter(Items.item_name == '').delete()


class Expenses(Base):
    """Base user class"""
    __tablename__ = "expenses"
    expense_id = Column(Integer, primary_key=True)
    item_id = Column(Integer)
    value = Column(Float)
    date = Column(String)

    def __init__(self, **kwargs):
        self.expense_id = kwargs['expense_id']
        self.item_id = kwargs['item_id']
        self.value = kwargs['value']
        self.date = kwargs['date']

    def get_expenses(**kwargs):
        date_type = kwargs['date_type']
        query_date = kwargs['date']

        with session_scope() as session:

            if date_type == 'day':
                expenses = session.query(Expenses.expense_id, Items.item_name, Expenses.value, Expenses.date)\
                    .filter(Items.item_id == Expenses.item_id).filter(Expenses.date == query_date).all()
                expense_dict = {}
                for expense in expenses:
                    expense_dict[expense.expense_id] = {'item_name': expense.item_name,
                                                        'value': expense.value,
                                                        'date': expense.date}

            elif date_type == 'month':
                month = query_date.strftime("%m")
                year = query_date.strftime("%Y")
                expenses = session.query(Expenses.date, func.sum(Expenses.value))\
                    .filter(Expenses.date.like('%{}-{}-%'.format(year, month)))\
                    .group_by(Expenses.date).all()
                expense_dict = {}
                for expense in expenses:
                    expense_dict[expense.date] = expense[1]

            elif date_type == 'year':
                query_year = int(query_date.strftime("%Y"))
                expenses = session.query(Expenses).all()
                expense_dict = {}
                for expense in expenses:
                    ex_date = datetime.strptime(expense.date, '%Y-%m-%d')
                    if ex_date.year == query_year:
                        if ex_date.strftime('%b') in expense_dict.keys():
                            expense_dict[ex_date.strftime('%b')] = expense_dict[ex_date.strftime('%b')] + expense.value
                        else:
                            expense_dict[ex_date.strftime('%b')] = expense.value

            return expense_dict

    def add_expense(**kwargs):
        with session_scope() as session:
            expense = Expenses(**kwargs)
            session.add(expense)

    def del_expense(**kwargs):
        expense_id = kwargs['expense_id']
        with session_scope() as session:
            session.query(Expenses).filter(Expenses.expense_id == expense_id).delete()

    def get_next_exp_id():
        with session_scope() as session:
            expense_id = session.query(func.max(Expenses.expense_id)).one()[0]
        if expense_id is None:
            expense_id = 1
        else:
            expense_id = expense_id + 1
        return expense_id

    def get_borders():
        expense_dict = {'MEDay':   {'date': '1900-01-01', 'value': 0.0},
                        'LEDay':   {'date': '1900-01-01', 'value': 0.0},
                        'LEMonth':   {'date': '1900-01', 'value': 0.0},
                        'MEMonth': {'date': '1900-01', 'value': 0.0}
                        }
        with session_scope() as session:
            expense = session.query(Expenses.date, func.sum(Expenses.value).label('value_sum'))\
                .having(text("value_sum > 0"))\
                .group_by(Expenses.date).order_by(desc('value_sum')).first()
            if expense is not None:
                expense_dict['MEDay'] = {'date': expense[0], 'value': expense[1]}

            expense = session.query(Expenses.date, func.sum(Expenses.value).label('value_sum')) \
                .having(text("value_sum > 0")) \
                .group_by(Expenses.date).order_by('value_sum').first()
            if expense is not None:
                expense_dict['LEDay'] = {'date': expense[0], 'value': expense[1]}

            expense = session.query(func.substr(Expenses.date, 1, 7).label('month'),
                                    func.sum(Expenses.value).label('value_sum')) \
                .having(text("value_sum > 0")) \
                .group_by('month').order_by('value_sum').first()
            if expense is not None:
                expense_dict['LEMonth'] = {'date': expense[0], 'value': expense[1]}

            expense = session.query(func.substr(Expenses.date, 1, 7).label('month'),
                                    func.sum(Expenses.value).label('value_sum')) \
                .having(text("value_sum > 0")) \
                .group_by('month').order_by(desc('value_sum')).first()
            if expense is not None:
                expense_dict['MEMonth'] = {'date': expense[0], 'value': expense[1]}

        return expense_dict

    def get_totals(q_date):
        query_date = q_date.strftime('%Y-%m-%d')
        query_month = query_date[0:7]
        query_year = query_date[0:4]
        totals = {'day': 0.0, 'month': 0.0, 'year': 0.0}
        with session_scope() as session:
            day_total = session.query(func.sum(Expenses.value)) \
                .filter(Expenses.date == query_date).group_by(Expenses.date).first()
            if day_total is not None:
                totals['day'] = day_total[0]

            month_query = session.query(func.substr(Expenses.date, 1, 7).label('month'),
                                        func.sum(Expenses.value).label('value_sum')) \
                .group_by('month')
            month_subquery = month_query.subquery()
            month_total = session.query(month_subquery.c.value_sum)\
                .filter(month_subquery.c.month == query_month).first()
            if month_total is not None:
                totals['month'] = month_total[0]

            year_query = session.query(func.substr(Expenses.date, 1, 4).label('year'),
                                       func.sum(Expenses.value).label('value_sum')) \
                .group_by('year')
            year_subquery = year_query.subquery()
            year_total = session.query(year_subquery.c.value_sum)\
                .filter(year_subquery.c.year == query_year).first()
            if year_total is not None:
                totals['year'] = year_total[0]

        return totals

    def get_avgs():
        expense_dict = {}
        with session_scope() as session:
            expense_query = session.query(Expenses.date, func.sum(Expenses.value).label('value_sum')) \
                .having(text("value_sum > 0")) \
                .group_by(Expenses.date).subquery()
            expense = session.query(func.avg(expense_query.c.value_sum)).first()
            if expense[0] is not None:
                expense_dict['day_avg'] = expense[0]
            else:
                expense_dict['day_avg'] = 0.0

            expense_query = session.query(func.substr(Expenses.date, 1, 7).label('month'),
                                          func.sum(Expenses.value).label('value_sum')) \
                .having(text("value_sum > 0")) \
                .group_by('month').subquery()
            expense = session.query(func.avg(expense_query.c.value_sum)).first()
            if expense[0] is not None:
                expense_dict['month_avg'] = expense[0]
            else:
                expense_dict['month_avg'] = 0.0

            expense_query = session.query(func.substr(Expenses.date, 1, 4).label('year'),
                                       func.sum(Expenses.value).label('value_sum')) \
                .having(text("value_sum > 0")) \
                .group_by('year').subquery()
            expense = session.query(func.avg(expense_query.c.value_sum)).first()
            if expense[0] is not None:
                expense_dict['year_avg'] = expense[0]
            else:
                expense_dict['year_avg'] = 0.0

        return expense_dict




