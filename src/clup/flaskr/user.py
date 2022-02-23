import json                                                                                                  
import datetime                                                                                              
                                                                                                             
from flask import Blueprint, render_template, request, jsonify, abort, flash, redirect, url_for              
from flask_login import login_required, current_user                                                         
                                                                                                             
import src.clup.flaskr.global_setup as setup                                                                 
from src.clup.entities.category import Category                                                              
from src.clup.entities.exceptions import MaxCapacityReachedError                                             
from src.clup.usecases.filter_aisle_by_categories_usecase import FilterAisleByCategoriesUseCase              
from src.clup.usecases.get_store_categories import GetStoreCategoriesUseCase                                 
from src.clup.usecases.load_store_info_usecase import LoadStoreInfoUseCase                                   
from src.clup.usecases.load_user_usecase import LoadUserUseCase                                              
from src.clup.usecases.load_user_reservations_data_usecase import LoadUserReservationsDataUseCase                                                                   
from src.clup.usecases.make_appointment_usecase import MakeAppointmentUseCase                                
from src.clup.usecases.make_reservation_usecase import MakeReservationUseCase                                
from src.clup.usecases.search_store_usecase import SearchStoreUseCase                                        
                                                                                                             
bp = Blueprint('user', __name__)                                                                             
                                                                                                             
                                                                                                             
@bp.route('/user/home')                                                                                      
@login_required                                                                                              
def home():                                                                                                  
    u_id = current_user.get_id()                                                                             
    user_data = LoadUserUseCase(setup.user_provider).execute(u_id)                                           
    return render_template('user/home.html', user=user_data)                                                 
                                                                                                             
                                                                                                             
@bp.route('/user/account')                                                                                   
@login_required                                                                                              
def account():                                                                                               
    return '<h1>User Account Page</h1>'                                                                      
                                                                                                             
                                                                                                             
@bp.route('/user/stores')                                                                                    
@login_required                                                                                              
def search_stores():                                                                                         
    args = request.args                                                                                      
    name = args.get('name', default='', type=str)                                                            
    u = SearchStoreUseCase(setup.store_provider)                                                             
    store_list = u.execute(name)                                                                             
    return jsonify(store_list)                                                                               
                                                                                                             
                                                                                                             
@bp.route('/user/stores/<store_id>')                                                                         
@login_required                                                                                              
def store_info(store_id):                                                                                    
    u_id = current_user.get_id()                                                                             
    user_data = LoadUserUseCase(setup.user_provider).execute(u_id)                                           
    u = LoadStoreInfoUseCase(setup.store_provider, setup.aisle_provider)                                     
    info = u.execute(store_id)                                                                               
    gsc = GetStoreCategoriesUseCase(setup.aisle_provider)                                                    
    categories = gsc.execute(store_id)                                                                       
    return render_template('user/store.html', user=user_data,                                                
                           store=info['store'], aisles=info['aisles'], categories=categories)                
                                                                                                             
                                                                                                             
@bp.route('/user/stores/<store_id>/slots')                                                                   
@login_required                                                                                              
def store_time_slots(store_id):                                                                              
    return '<h1>User Store Time Slots Page</h1>'                                                             
                                                                                                             
                                                                                                             
@bp.route('/user/reservations/<store_id>', methods=['POST'])                                                 
@login_required                                                                                              
def make_reservation(store_id):                                                                              
    user_id = current_user.get_id()                                                                          
    categories = request.values['categories']                                                                
    try:                                                                                                     
        categories_json = json.loads(categories)                                                             
        categories_enum = [Category(int(c)) for c in categories_json]                                        
        fabc = FilterAisleByCategoriesUseCase(setup.aisle_provider)                                          
        aisle_ids_json = fabc.execute(store_id, categories_enum)                                             
    except json.JSONDecodeError:                                                                             
        abort(400)                                                                                           
                                                                                                             
    mru = MakeReservationUseCase(setup.lane_provider,                                                        
                                 setup.reservation_provider)                                                 
    mru.execute(user_id, store_id, aisle_ids_json)                                                           
    for aisle_id in aisle_ids_json:                                                                          
        pool = setup.lane_provider.get_aisle_pool(aisle_id)                                                  
        queue = setup.lane_provider.get_waiting_queue(aisle_id)                                              
        print(f'{aisle_id} - {pool.capacity} - {pool.current_quantity}')                                     
        print(list(queue))                                                                                   
        print(list(pool))                                                                                    
    return '', 200                                                                                           
                                                                                                             
                                                                                                             
@bp.route('/user/reservations', methods=['GET', 'POST'])                                                     
@login_required                                                                                              
def reservations():                                                                                          
    u_id = current_user.get_id()                                                                             
    user_data = LoadUserUseCase(setup.user_provider).execute(u_id)                                           
    lurdu = LoadUserReservationsDataUseCase(setup.reservation_provider,                                      
                                            setup.store_provider,                                            
                                            setup.aisle_provider)                                            
    stores_with_aisles = lurdu.execute(u_id)                                                                 
    return render_template('user/reservations.html', user=user_data,                                         
                           stores_with_aisles=stores_with_aisles)                                            
                                                                                                             
                                                                                                             
@bp.route('/user/stores/<store_id>/appointment', methods=['GET', 'POST'])                                    
@login_required                                                                                              
def make_appointment(store_id):                                                                              
    u_id = current_user.get_id()                                                                             
    user_data = LoadUserUseCase(setup.user_provider).execute(u_id)                                           
    u = LoadStoreInfoUseCase(setup.store_provider, setup.aisle_provider)                                     
    info = u.execute(store_id)                                                                               
    gsc = GetStoreCategoriesUseCase(setup.aisle_provider)                                                    
    categories = gsc.execute(store_id)                                                                       
    if request.method == 'POST':                                                                             
        try:                                                                                                 
            categories = request.values['categories']                                                        
            categories_json = json.loads(categories)                                                         
            categories_enum = [Category(int(c)) for c in categories_json]                                    
            fabc = FilterAisleByCategoriesUseCase(setup.aisle_provider)                                      
            aisle_ids_json = fabc.execute(store_id, categories_enum)                                         
            datetime_from_req = request.values['datetime']                                                   
            date, time = datetime_from_req.split('T')                                                        
            year, month, day = date.split('-')                                                               
            hour = time.split(':')[0]                                                                        
            mauc = MakeAppointmentUseCase(setup.reservation_provider,                                        
                                          setup.appointment_provider,                                        
                                          setup.aisle_provider)                                              
                                                                                                                                                                                                            
        except json.JSONDecodeError:                                                                         
            abort(400)

        try:
            mauc.execute(                                                                                    
                    store_id=store_id,                                                                           
                    aisle_ids=aisle_ids_json,                                                                    
                    date=datetime.datetime(int(year), int(month), int(day), int(hour)),                          
                    user_id=u_id                                                                                 
                )
            return '',200
        except MaxCapacityReachedError:                                                                                                                                              
            flash("not enough space in this time slot, try with another", category='danger')  
            print("MaxCapacity")               
            return '',400                                                           
    return render_template('user/appointment.html', user=user_data, store_id=store_id, store=info['store'],  
                           categories=categories) 