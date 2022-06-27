# Architecture #

Collection of different diagrams

### Architecture diagram ###

![Architecture diagram](images/ros2.drawio.png)

### Camera node ###

```
,------------------------------------------------------------.
|workspace.src.camera_node.camera_node.camera_node.CameraNode|
|------------------------------------------------------------|
|timer:                                                      |
|cap:                                                        |
|publisher:                                                  |
|bridge:                                                     |
|__init__(self):                                             |
|publish_image(self):                                        |
`------------------------------------------------------------'
                               |                              
                               |                              
                            ,----.                            
                            |Node|                            
                            |----|                            
                            `----'                            
```

### I/O node ###

```
,--------------------------------------------.                                                                                                                                                                                       
|workspace.src.io_node.io_node.io_node.IONode|                                                                                                                                                                                       
|--------------------------------------------|                                                                                                                                                                                       
|timer:                                      |                                                                                                                                                                                       
|view:                                       |                                                                                                                                                                                       
|main_menu:                                  |                                                                                                                                                                                       
|qr_menu_publisher:                          |                                                                                                                                                                                       
|log_subscription_:                          |                                                                                                                                                                                       
|exploration_publisher:                      |                                                                                                                                                                                       
|qr_menu:                                    |                                                                                                                                                                                       
|manual_control:                             |                                                                                                                                                                                       
|qr_code_subscription_:                      |                                                                                                                                                                                       
|__init__(self):                             |                                                                                                                                                                                       
|load_view(self, view):                      |                                                                                                                                                                                       
|check_quit(self):                           |                                                                                                                                                                                       
|log(self, msg: String):                     |                                                                                                                                                                                       
`--------------------------------------------'                                                                                                                                                                                       
                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                     
                               ,-----------------------------------------------------------.                                                                                                                                         
                               |workspace.src.io_node.io_node.submodules.main_menu.MainMenu|                                                                            ,-----------------------------------------------------------.
                               |-----------------------------------------------------------|                                                                            |workspace.src.io_node.io_node.submodules.qr_menu.QRMenu    |
                               |running:                                                   |                                                                            |-----------------------------------------------------------|
                               |_data_to_log:                                              |   ,---------------------------------------------------------------------.  |running:                                                   |
                               |_load_manual_control_view:                                 |   |workspace.src.io_node.io_node.submodules.manual_control.ManualControl|  |_data_to_log:                                              |
                               |_publisher:                                                |   |---------------------------------------------------------------------|  |_stop_exploring:                                           |
                               |thread:                                                    |   |running:                                                             |  |_qr_codes:                                                 |
                               |_load_qr_view:                                             |   |_return_to_menu:                                                     |  |_reprint_menu:                                             |
                               |__init__(self, publisher: Callable[[String], None]):       |   |__init__(self, return_to_menu):                                      |  |_publisher:                                                |
                ,----.         |set_load_functions(                                        |   |open(self):                                                          |  |thread:                                                    |
                |Node|         |     self,                                                 |   |close(self):                                                         |  |_return_to_menu:                                           |
                |----|         |     load_manual_control_view: Callable[[], None],         |   |_get_key(self, settings):                                            |  |__init__(self, return_to_menu, stop_exploring, publisher): |
                `----'         |     load_qr_view: Callable[[], None],                     |   |_print_vels(self, target_linear_velocity, target_angular_velocity):  |  |open(self):                                                |
                               | ):                                                        |   |_make_simple_profile(self, output, input, slop):                     |  |close(self):                                               |
                               |open(self):                                                |   |_constrain(self, input_vel, low_bound, high_bound):                  |  |log(self, data: str):                                      |
                               |close(self):                                               |   |_check_linear_limit_velocity(self, velocity):                        |  |qr_listener_callback(self, qr_code: QRCode):               |
                               |log(self, data: str):                                      |   |_check_angular_limit_velocity(self, velocity):                       |  |_qr_navigation_callback(self, qr_code: QRCode):            |
                               |_exploration_callback(self, msg_command: String):          |   |_main(self):                                                         |  |_get_key(self, settings):                                  |
                               |_get_key(self, settings):                                  |   `---------------------------------------------------------------------'  |_print_menu(self):                                         |
                               |_print_menu(self):                                         |                                                                            |_handle_io(self):                                          |
                               |_handle_io(self):                                          |                                                                            |_main(self):                                               |
                               |_main(self):                                               |                                                                            `-----------------------------------------------------------'
                               `-----------------------------------------------------------'                                                                                                                                         
                                                             |                                                                                                                                                                       
                                     ,----------------------------------------------.                                                                                                                                                
                                     |object                                        |                                                                                                                                                
                                     |----------------------------------------------|                                                                                                                                                
                                     |__doc__:                                      |                                                                                                                                                
                                     |__dict__:                                     |                                                                                                                                                
                                     |__slots__:                                    |                                                                                                                                                
                                     |__module__:                                   |                                                                                                                                                
                                     |__annotations__:                              |                                                                                                                                                
                                     |__class__(self: _T):                          |                                                                                                                                                
                                     |__class__(self, __type: Type[object]):        |                                                                                                                                                
                                     |__init__(self):                               |                                                                                                                                                
                                     |__new__(cls: Type[_T]):                       |                                                                                                                                                
                                     |__setattr__(self, name: str, value: Any):     |                                                                                                                                                
                                     |__eq__(self, o: object):                      |                                                                                                                                                
                                     |__ne__(self, o: object):                      |                                                                                                                                                
                                     |__str__(self):                                |                                                                                                                                                
                                     |__repr__(self):                               |                                                                                                                                                
                                     |__hash__(self):                               |                                                                                                                                                
                                     |__format__(self, format_spec: str):           |                                                                                                                                                
                                     |__getattribute__(self, name: str):            |                                                                                                                                                
                                     |__delattr__(self, name: str):                 |                                                                                                                                                
                                     |__sizeof__(self):                             |                                                                                                                                                
                                     |__reduce__(self):                             |                                                                                                                                                
                                     |__reduce_ex__(self, protocol: SupportsIndex): |                                                                                                                                                
                                     |__reduce_ex__(self, protocol: int):           |                                                                                                                                                
                                     |__dir__(self):                                |                                                                                                                                                
                                     |__init_subclass__(cls):                       |                                                                                                                                                
                                     `----------------------------------------------'                                                                                                                                                
                                                             |                                                                                                                                                                       
                                                                                                                                                                                                                                     
                                                    ,----------------.                                                                                                                                                               
                                                    |typing.Hashable |                                                                                                                                                               
                                                    |----------------|                                                                                                                                                               
                                                    |__hash__(self): |                                                                                                                                                               
                                                    `----------------'                                                                                                                                                               
```

### Database schema ###

```
,----------------------.                          
|history               |  ,----------------------.
|----------------------|  |qr_codes              |
|id: int               |  |----------------------|
|center_x: float       |  |center_x: float       |
|center_y: float       |  |center_y: float       |
|center_z: float       |  |center_z: float       |
|normal_vector_x: float|  |normal_vector_x: float|
|normal_vector_y: float|  |normal_vector_y: float|
|normal_vector_z: float|  |normal_vector_z: float|
|rotation_w: float     |  |rotation_w: float     |
|rotation_x: float     |  |rotation_x: float     |
|rotation_y: float     |  |rotation_y: float     |
|rotation_z: float     |  |rotation_z: float     |
|time: timestamp       |  |id: int               |
|pk: int               |  `----------------------'
`----------------------'                          
                                                  
                                                  
    ,--------------.                              
    |sqlite_master |                              
    |--------------|                              
    |type: text    |                              
    |name: text    |                              
    |tbl_name: text|                              
    |rootpage: int |                              
    |sql: text     |                              
    `--------------'                              
```

### Memory node ###

```
                                                                                                                                                      ,--------------------------------------------------------------.
                                                                                                                                                      |workspace.src.memory_node.test.memory_node_test.MemoryNodeTest|
                                                                                                                                                      |--------------------------------------------------------------|
                                                                                                                                                      |delay:                                                        |
,---------------------------------------------------------------------.                                                                               |test_node:                                                    |
|workspace.src.memory_node.memory_node.memory_node.MemoryNode         |                  ,--------------------------------------------------------.   |qr_code:                                                      |
|---------------------------------------------------------------------|                  |workspace.src.memory_node.test.memory_node_test.NodeNode|   |executor_thread:                                              |
|srv:                                                                 |                  |--------------------------------------------------------|   |memory_node:                                                  |
|publisher:                                                           |                  |future:                                                 |   |setUpClass(self):                                             |
|qr_code_subscription:                                                |                  |publisher:                                              |   |setUp(self):                                                  |
|__init__(self):                                                      |                  |client:                                                 |   |tearDownClass(self):                                          |
|add_qr_code_callback(self, qr_code: QRCode):                         |                  |__init__(self):                                         |   |assert_qr_codes_equal(                                        |
|get_qr_codes_callback(                                               |                  |add_qr_code(self, qr_code: QRCode):                     |   |     self,                                                    |
|     self, request: GetQRCodes.Request, response: GetQRCodes.Response|                  |get_qr_codes(self):                                     |   |     qr_code_1: QRCode,                                       |
| ):                                                                  |                  `--------------------------------------------------------'   |     qr_code_2: QRCode,                                       |
`---------------------------------------------------------------------'                                                                               | ):                                                           |
                                                                                                                                                      |test_getting_data_when_no_qr_codes_have_been_added(self):     |
                                                                                                                                                      |test_adding_data(self):                                       |
                                                                                                                                                      `--------------------------------------------------------------'
                                                                                                                                                                                                                      
                                                                                                                                                                                                                      
                                             ,-------------------------------------------------------------------------------.                                                                                        
                                             |workspace.src.memory_node.memory_node.submodules.data_repository.DataRepository|                                                                                        
                                             |-------------------------------------------------------------------------------|                                                                                        
                                    ,----.   |__init__(self):                                                                |                                                                                        
                                    |Node|   |qr_code_to_dict(qr_code: QRCode):                                              |                                                                                        
                                    |----|   |row_to_qr_code(row: List):                                                     |                                                                                        
                                    `----'   |add_qr_code_to_history(self, qr_code: QRCode):                                 |                                                                                        
                                             |add_qr_code(self, qr_code: QRCode):                                            |                                                                                        
                                             |get_qr_codes(self):                                                            |                                                                                        
                                             |delete_all(self):                                                              |                                                                                        
                                             `-------------------------------------------------------------------------------'                                                                                        
                                                                                                                                                                                                                      
                                      ,----------------------------------------------.                                                                                                                                
                                      |object                                        |                                                                                                                                
                                      |----------------------------------------------|                                                                                                                                
                                      |__doc__:                                      |                                                                                                                                
                                      |__dict__:                                     |                                                                                                                                
                                      |__slots__:                                    |                                                                                                                                
                                      |__module__:                                   |                                                                                                                                
                                      |__annotations__:                              |                                                                                                                                
                                      |__class__(self: _T):                          |                                                                                                                                
                                      |__class__(self, __type: Type[object]):        |                                                                                                                                
                                      |__init__(self):                               |                                                                                                                                
                                      |__new__(cls: Type[_T]):                       |                                                                                                                                
                                      |__setattr__(self, name: str, value: Any):     |                                                                                                                                
                                      |__eq__(self, o: object):                      |                                                                                                                                
                                      |__ne__(self, o: object):                      |                                                                                                                                
                                      |__str__(self):                                |                                                                                                                                
                                      |__repr__(self):                               |                                                                                                                                
                                      |__hash__(self):                               |                                                                                                                                
                                      |__format__(self, format_spec: str):           |                                                                                                                                
                                      |__getattribute__(self, name: str):            |                                                                                                                                
                                      |__delattr__(self, name: str):                 |                                                                                                                                
                                      |__sizeof__(self):                             |                                                                                                                                
                                      |__reduce__(self):                             |                                                                                                                                
                                      |__reduce_ex__(self, protocol: SupportsIndex): |                                                                                                                                
                                      |__reduce_ex__(self, protocol: int):           |                                                                                                                                
                                      |__dir__(self):                                |                                                                                                                                
                                      |__init_subclass__(cls):                       |                                                                                                                                
                                      `----------------------------------------------'                                                                                                                                
                                                              |                                                                                                                                                       
                                                                                                                                                                                                                      
                                                     ,----------------.                                                                                                                                               
                                                     |typing.Hashable |                                                                                                                                               
                                                     |----------------|                                                                                                                                               
                                                     |__hash__(self): |                                                                                                                                               
                                                     `----------------'                                                                                                                                               
```

### QR reader ###

```
,-----------------------------------------------------------------------------.                                                                                                                                       
|workspace.src.qr_code_reader.qr_code_reader.qr_code_reader.QRCodeReader      |                                                                                                                                       
|-----------------------------------------------------------------------------|                                                                                                                                       
|get_position:                                                                |                                                                                                                                       
|qr_code_cache:                                                               |                                                                                                                                       
|camera_position:                                                             |                                                                                                                                       
|tf_listener:                                                                 |                                                                                                                                       
|rotation:                                                                    |                                                                                                                                       
|tf_buffer:                                                                   |                                                                                                                                       
|threshold:                                                                   |                                                                                                                                       
|subscription:                                                                |                                                                   ,------------------------------------------------------------------.
|cache_time:                                                                  |                                                                   |workspace.src.qr_code_reader.test.qr_code_node_test.QRCodeNodeTest|
|cv_bridge:                                                                   |                                                                   |------------------------------------------------------------------|
|future:                                                                      |                                                                   |delay:                                                            |
|qr_code_client:                                                              |                                                                   |subscriber:                                                       |
|log_publisher:                                                               |                                                                   |qr_code_reader_node:                                              |
|last_update:                                                                 |  ,------------------------------------------------------------.   |test_node:                                                        |
|rotation_offset:                                                             |  |workspace.src.qr_code_reader.test.qr_code_node_test.NodeNode|   |qr_code:                                                          |
|camera_vector:                                                               |  |------------------------------------------------------------|   |executor_thread:                                                  |
|publisher:                                                                   |  |publisher:                                                  |   |setUpClass(self):                                                 |
|position:                                                                    |  |bridge:                                                     |   |setUp(self):                                                      |
|__init__(                                                                    |  |subscription:                                               |   |tearDownClass(self):                                              |
|     self,                                                                   |  |__init__(self, subscriber_callback):                        |   |assert_qr_codes_equal(                                            |
|     threshold: float = TF_THRESHOLD,                                        |  |send_image(self, image_filename: str):                      |   |     self,                                                        |
|     get_position: Callable[[], Optional[Tuple[Vector3, Quaternion]]] = None,|  `------------------------------------------------------------'   |     qr_code_1: QRCode,                                           |
| ):                                                                          |                                                                   |     qr_code_2: QRCode,                                           |
|undistort_image(self, image: ndarray):                                       |                                                                   | ):                                                               |
|detect_code(self, image: ndarray):                                           |                                                                   |test_sending_image_without_a_qr_code(self):                       |
|get_vectors(self, points: List):                                             |                                                                   |test_sending_image_with_a_qr_code(self):                          |
|get_position_from_tf(                                                        |                                                                   |test_sending_image_with_the_same_qr_code_twice(self):             |
|     self,                                                                   |                                                                   |test_sending_image_twice_but_changing_robot_position(self):       |
| ):                                                                          |                                                                   `------------------------------------------------------------------'
|update_position(self):                                                       |                                                                                                                                       
|update_qr_code_cache(self):                                                  |                                                                                                                                       
|spin(self):                                                                  |                                                                                                                                       
|calculate(                                                                   |                                                                                                                                       
|     self, points: List[ndarray]                                             |                                                                                                                                       
| ):                                                                          |                                                                                                                                       
|image_callback(self, msg_image: Image):                                      |                                                                                                                                       
|reset_found_codes(self):                                                     |                                                                                                                                       
`-----------------------------------------------------------------------------'                                                                                                                                       
                                                                                                                                                                                                                      
                                                                                                                                                                                                                      
                                                                                                      ,--------------------------------------------------------------.                                                
                                                                                       ,----.         |workspace.src.qr_code_reader.test.qr_code_node_test.Subscriber|                                                
                                                                                       |Node|         |--------------------------------------------------------------|                                                
                                                                                       |----|         |calls:                                                        |                                                
                                                                                       `----'         |__init__(self):                                               |                                                
                                                                                                      |callback(self, qr_code: QRCode):                              |                                                
                                                                                                      `--------------------------------------------------------------'                                                
                                                                                                                                                                                                                      
                                                                      ,----------------------------------------------.                                                                                                
                                                                      |object                                        |                                                                                                
                                                                      |----------------------------------------------|                                                                                                
                                                                      |__doc__:                                      |                                                                                                
                                                                      |__dict__:                                     |                                                                                                
                                                                      |__slots__:                                    |                                                                                                
                                                                      |__module__:                                   |                                                                                                
                                                                      |__annotations__:                              |                                                                                                
                                                                      |__class__(self: _T):                          |                                                                                                
                                                                      |__class__(self, __type: Type[object]):        |                                                                                                
                                                                      |__init__(self):                               |                                                                                                
                                                                      |__new__(cls: Type[_T]):                       |                                                                                                
                                                                      |__setattr__(self, name: str, value: Any):     |                                                                                                
                                                                      |__eq__(self, o: object):                      |                                                                                                
                                                                      |__ne__(self, o: object):                      |                                                                                                
                                                                      |__str__(self):                                |                                                                                                
                                                                      |__repr__(self):                               |                                                                                                
                                                                      |__hash__(self):                               |                                                                                                
                                                                      |__format__(self, format_spec: str):           |                                                                                                
                                                                      |__getattribute__(self, name: str):            |                                                                                                
                                                                      |__delattr__(self, name: str):                 |                                                                                                
                                                                      |__sizeof__(self):                             |                                                                                                
                                                                      |__reduce__(self):                             |                                                                                                
                                                                      |__reduce_ex__(self, protocol: SupportsIndex): |                                                                                                
                                                                      |__reduce_ex__(self, protocol: int):           |                                                                                                
                                                                      |__dir__(self):                                |                                                                                                
                                                                      |__init_subclass__(cls):                       |                                                                                                
                                                                      `----------------------------------------------'                                                                                                
                                                                                              |                                                                                                                       
                                                                                                                                                                                                                      
                                                                                     ,----------------.                                                                                                               
                                                                                     |typing.Hashable |                                                                                                               
                                                                                     |----------------|                                                                                                               
                                                                                     |__hash__(self): |                                                                                                               
                                                                                     `----------------'                                                                                                               
```

### Explore node ###

```
,--------------------------------------------------------------------.
|workspace.src.explore_node.explore_node.explore_node.ExploreNode    |
|--------------------------------------------------------------------|
|map_origin:                                                         |
|nav:                                                                |
|commander_subscription:                                             |
|go_to_qr_code_subscription:                                         |
|robot_position:                                                     |
|map_resolution:                                                     |
|tf_listener:                                                        |
|searching:                                                          |
|map_width:                                                          |
|previous_target:                                                    |
|pos_y:                                                              |
|start_time:                                                         |
|pos_x:                                                              |
|map_occupancy_listener:                                             |
|map_height:                                                         |
|retrace_index:                                                      |
|initial_pose:                                                       |
|retrace_coordinates:                                                |
|map_set:                                                            |
|map:                                                                |
|retracing:                                                          |
|__init__(self, nav: BasicNavigator):                                |
|go_to_qr_code(self, qrcode: QRCode):                                |
|commander_callback(self, msg: String):                              |
|map_listener_callback(self, occupancy_grid: OccupancyGrid):         |
|tf_listener_callback(self, msg: TFMessage):                         |
|set_initial_pose(self, translation: Vector3, rotation: Quaternion): |
|make_map(self):                                                     |
|find_target(self, map: List[List[int]]):                            |
|transform_coordinates_into_grid(self):                              |
|breadth_first_search(                                               |
|     self, map: List[List[int]], start_x: int, start_y: int         |
| ):                                                                 |
|cancel_explore(self):                                               |
|start_explore(self):                                                |
|explore(self):                                                      |
|retrace(self):                                                      |
|move(self, x: float, y: float):                                     |
|move_and_spin(self, x: float, y: float):                            |
`--------------------------------------------------------------------'
                                   |                                  
                                   |                                  
                                ,----.                                
                                |Node|                                
                                |----|                                
                                `----'                                
```