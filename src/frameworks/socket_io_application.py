from flask import Flask
from flask_socketio import SocketIO
from flask_socketio import emit, join_room, leave_room

# Room constants
EMPLOYEE_ROOM = "employee_room"

class SocketIOApplication:
    def __init__(self, flask: Flask):
        self.io = SocketIO(cors_allowed_origins="*")
        self.io.init_app(flask)

        @self.io.on("connect")
        def handle_connect():
            print("Client connected")
            self.io.emit("response", {"message": "Connected successfully!"})

        @self.io.on("disconnect")
        def handle_disconnect():
            print("Client disconnected")
            pass

        # CUSTOMER EVENTS
        @self.io.on("customer_join")
        def customer_join(data):
            """
            Handle customer joining the system.
            """
            customer_id = data.get("customer_id")
            if not customer_id:
                return emit("error", {"message": "Customer ID is required"})
            
            join_room(EMPLOYEE_ROOM)
            print(f"Customer {customer_id} joined their room.")
            emit("response", {"message": f"Customer {customer_id} joined."})

        @self.io.on("customer_order")
        def customer_order(data):
            """
            Handle customer placing an order.
            """
            customer_id = data.get("customer_id")
            order_info = data.get("order_info")
            
            if not customer_id or not order_info:
                return emit("error", {"message": "Customer ID and order info are required"})
            
            print(f"Customer {customer_id} placed an order: {order_info}")
            
            # Broadcast order to all employees
            emit("new_order", {"customer_id": customer_id, "order_info": order_info}, room=EMPLOYEE_ROOM)

        # EMPLOYEE EVENTS
        @self.io.on("employee_join")
        def employee_join(data):
            """
            Handle employee joining the employee room.
            """
            employee_id = data.get("employee_id")
            if not employee_id:
                return emit("error", {"message": "Employee ID is required"})
            
            join_room(EMPLOYEE_ROOM)
            print(f"Employee {employee_id} joined the employee room.")
            emit("response", {"message": f"Employee {employee_id} joined the room."}, room=EMPLOYEE_ROOM)

        @self.io.on("private_message")
        def private_message(data):
            """
            Exchange private messages between customer and employee.
            """
            customer_id = data.get("customer_id")
            employee_id = data.get("employee_id")
            order_id = data.get("order_id")
            print("Hehe")
            emit("message", {"customer_id": customer_id, "employee_id": employee_id, "order_id": order_id}, room=EMPLOYEE_ROOM)

        @self.io.on("send_location")
        def send_location(data):
            """
            Send employee's location to customer.
            """
            customer_id = data.get("customer_id")
            order_id = data.get("order_id")
            lat = data.get("lat")
            long = data.get("long")
            emit("get_location", {"customer_id": customer_id, "order_id": order_id, "lat": lat, "long": long}, room=EMPLOYEE_ROOM)
