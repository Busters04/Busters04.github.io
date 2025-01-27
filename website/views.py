from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from bson.objectid import ObjectId
from .database import spiritualGoalsCol, mentalGoalsCol, physicalGoalsCol, completionsCol
import datetime
import pytz  # <--- NEW

views = Blueprint('views', __name__)

@views.route('/')
def home():
    if 'user_id' not in session:
        flash('You must be logged in to view the home page.', 'error')
        return redirect(url_for('auth.login'))
    return render_template('home.html')

@views.route('/spiritual')
def spiritual():
    if 'user_id' not in session:
        flash('You must be logged in to view this page.', 'error')
        return redirect(url_for('auth.login'))
    return render_template('home.html', tab='spiritual')

@views.route('/mental')
def mental():
    if 'user_id' not in session:
        flash('You must be logged in to view this page.', 'error')
        return redirect(url_for('auth.login'))
    return render_template('home.html', tab='mental')

@views.route('/physical')
def physical():
    if 'user_id' not in session:
        flash('You must be logged in to view this page.', 'error')
        return redirect(url_for('auth.login'))
    return render_template('home.html', tab='physical')

############################################################################
#                          GOAL MANAGEMENT ROUTES                          #
############################################################################

@views.route('/goals/<category>', methods=['GET', 'POST'])
def manage_goals(category):
    """
    List all existing goals for a category (spiritual, mental, physical)
    and allow creation of a new goal with sub-goals.
    """
    if 'user_id' not in session:
        flash('You must be logged in.', 'error')
        return redirect(url_for('auth.login'))
    
    collections_map = {
        'spiritual': spiritualGoalsCol,
        'mental': mentalGoalsCol,
        'physical': physicalGoalsCol
    }
    if category not in collections_map:
        flash('Invalid category.', 'error')
        return redirect(url_for('views.home'))

    goals_collection = collections_map[category]
    user_id = session['user_id']

    if request.method == 'POST':
        goal_name = request.form.get('goal_name')
        main_start_date = request.form.get('start_date')  # 'YYYY-MM-DD'

        sub_goals = []
        sub_desc_list = request.form.getlist('sub_goal_description[]')
        sub_days_list = request.form.getlist('sub_goal_days_per_week[]')
        sub_start_list = request.form.getlist('sub_goal_start_date[]')

        for desc, days, sdate in zip(sub_desc_list, sub_days_list, sub_start_list):
            if desc.strip() == "" or days.strip() == "":
                continue
            sub_goals.append({
                "description": desc,
                "days_per_week": int(days),
                "start_date": datetime.datetime.strptime(sdate, '%Y-%m-%d') if sdate else None,
                "is_completed": False,
                "end_date": None
            })
        
        if not goal_name:
            flash('Please provide a goal name.', 'error')
        else:
            new_goal = {
                "user_id": user_id,
                "name": goal_name,
                "start_date": datetime.datetime.strptime(main_start_date, '%Y-%m-%d') if main_start_date else None,
                "is_completed": False,
                "end_date": None,
                "sub_goals": sub_goals,
                "created_at": datetime.datetime.utcnow()
            }
            goals_collection.insert_one(new_goal)
            flash(f'New {category} goal added!', 'success')
        return redirect(url_for('views.manage_goals', category=category))

    user_goals = list(goals_collection.find({'user_id': user_id}))
    return render_template('goals.html', category=category, goals=user_goals)


@views.route('/goals/<category>/<goal_id>/edit', methods=['GET', 'POST'])
def edit_goal(category, goal_id):
    if 'user_id' not in session:
        flash('You must be logged in.', 'error')
        return redirect(url_for('auth.login'))
    
    collections_map = {
        'spiritual': spiritualGoalsCol,
        'mental': mentalGoalsCol,
        'physical': physicalGoalsCol
    }
    if category not in collections_map:
        flash('Invalid category.', 'error')
        return redirect(url_for('views.home'))
    
    goals_collection = collections_map[category]
    user_id = session['user_id']

    goal = goals_collection.find_one({"_id": ObjectId(goal_id), "user_id": user_id})
    if not goal:
        flash("Goal not found or you don't have permission.", 'error')
        return redirect(url_for('views.manage_goals', category=category))

    if request.method == 'POST':
        main_is_completed = request.form.get('main_is_completed') == 'on'
        main_end_date = request.form.get('main_end_date')
        if main_end_date:
            try:
                main_end_date = datetime.datetime.strptime(main_end_date, '%Y-%m-%d')
            except ValueError:
                main_end_date = None
        else:
            main_end_date = None

        sub_goals = goal.get('sub_goals', [])
        for i, sub_goal in enumerate(sub_goals):
            is_completed_field = f'sub_{i}_completed'
            end_date_field = f'sub_{i}_end_date'

            sub_completed = request.form.get(is_completed_field) == 'on'
            sub_end_date_str = request.form.get(end_date_field)
            if sub_end_date_str:
                try:
                    sub_end_date = datetime.datetime.strptime(sub_end_date_str, '%Y-%m-%d')
                except ValueError:
                    sub_end_date = None
            else:
                sub_end_date = None

            sub_goal['is_completed'] = sub_completed
            sub_goal['end_date'] = sub_end_date

        goals_collection.update_one(
            {"_id": ObjectId(goal_id)},
            {
                "$set": {
                    "is_completed": main_is_completed,
                    "end_date": main_end_date,
                    "sub_goals": sub_goals
                }
            }
        )
        flash(f"{goal['name']} updated!", 'success')
        return redirect(url_for('views.manage_goals', category=category))

    return render_template('edit_goal.html', category=category, goal=goal)

############################################################################
#                           DAILY CHECK ROUTE                              #
############################################################################

@views.route('/daily-check', methods=['GET', 'POST'])
def daily_check():
    """
    - We use Arizona local time (America/Phoenix) to:
      1) Enforce one daily check per day (local date).
      2) Determine the weekly window (Mon 00:00 to Sun 23:59) in local time.
    - We store dates in UTC in the DB, but convert the local times to UTC for queries.
    """
    if 'user_id' not in session:
        flash('You must be logged in to do a daily check.', 'error')
        return redirect(url_for('auth.login'))

    # For Arizona time
    AZ = pytz.timezone('America/Phoenix')
    now_local = datetime.datetime.now(AZ)  # Current local AZ time

    user_id = session['user_id']

    # --------------- ENFORCE ONE DAILY CHECK PER DAY ---------------
    # "Today" in local AZ is from 00:00 to 23:59. If there's already a doc for that user in that range, deny access.

    # Get today's 00:00 in local AZ
    today_local = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
    # Next day 00:00 local AZ
    tomorrow_local = today_local + datetime.timedelta(days=1)

    # Convert those local times to UTC
    today_utc = today_local.astimezone(pytz.utc)
    tomorrow_utc = tomorrow_local.astimezone(pytz.utc)

    # Check if there's an existing record for the user in [today_utc, tomorrow_utc)
    existing_check = completionsCol.find_one({
        'user_id': user_id,
        'date': {
            '$gte': today_utc,
            '$lt': tomorrow_utc
        }
    })

    if request.method == 'GET':
        if existing_check:
            # User has already done a daily check today
            flash('You have already done your daily check for today!', 'info')
            return redirect(url_for('views.home'))
    else:
        # POST
        if existing_check:
            flash('You have already done your daily check for today!', 'info')
            return redirect(url_for('views.home'))
    
    # --------------- WEEKLY WINDOW (Mon 00:00 to Sun 23:59) in AZ ---------------
    weekday = now_local.weekday()  # Monday=0 ... Sunday=6
    # Calculate Monday 00:00 local
    monday_local = now_local - datetime.timedelta(days=weekday)
    monday_local = monday_local.replace(hour=0, minute=0, second=0, microsecond=0)
    # Sunday 23:59 local
    sunday_local = monday_local + datetime.timedelta(days=6, hours=23, minutes=59, seconds=59)

    # Convert them to UTC for DB query
    monday_utc = monday_local.astimezone(pytz.utc)
    sunday_utc = sunday_local.astimezone(pytz.utc)

    # Query all completions in [monday_utc, sunday_utc]
    recent_completions = list(completionsCol.find({
        'user_id': user_id,
        'date': {'$gte': monday_utc, '$lte': sunday_utc}
    }))

    # Build a map: (goal_id, sub_index) -> completion_count for this local week
    completion_counts = {}
    for record in recent_completions:
        for csg in record.get('completed_subgoals', []):
            key = (str(csg['goal_id']), csg['sub_index'])
            completion_counts[key] = completion_counts.get(key, 0) + 1

    # Fetch the user's goals
    spiritual_goals = list(spiritualGoalsCol.find({'user_id': user_id}))
    mental_goals = list(mentalGoalsCol.find({'user_id': user_id}))
    physical_goals = list(physicalGoalsCol.find({'user_id': user_id}))

    if request.method == 'POST':
        completed_list = request.form.getlist('completed_subgoals')
        completed_subgoals = []
        for item in completed_list:
            try:
                goal_id_str, sub_index_str = item.split('__')
                completed_subgoals.append({
                    'goal_id': ObjectId(goal_id_str),
                    'sub_index': int(sub_index_str)
                })
            except ValueError:
                continue

        # We'll store date in UTC (the "official" time)
        now_utc = datetime.datetime.utcnow()
        record = {
            'user_id': user_id,
            'date': now_utc,
            'completed_subgoals': completed_subgoals,
        }
        completionsCol.insert_one(record)

        flash('Daily check recorded!', 'success')
        return redirect(url_for('views.home'))

    return render_template(
        'daily_check.html',
        spiritual_goals=spiritual_goals,
        mental_goals=mental_goals,
        physical_goals=physical_goals,
        completion_counts=completion_counts
    )
