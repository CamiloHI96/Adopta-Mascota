from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'camilo123'

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Función para obtener la conexión a la base de datos
def get_db_connection():
    conn = None
    try:
        conn = sqlite3.connect('instance/adopta_mascotas.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Error de conexión a la base de datos: {e}")
        return None

# Ruta de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Ruta de inicio
@app.route('/index.html')
def inicio():
    return render_template('index.html')

# Ruta de login
@app.route('/login.html')
def logueo():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            user_obj = User(user['id'], user['email'], user['password'])
            login_user(user_obj)
            flash('Login successful!', 'success')
            return redirect(url_for('menu'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

# Ruta de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

# Ruta de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    email_exists = False
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['last-name']  # Nuevo campo para el apellido
        phone = request.form['phone']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        conn = get_db_connection()
        if conn:
            try:
                user_exists = conn.execute('SELECT 1 FROM users WHERE email = ?', (email,)).fetchone()
                if user_exists:
                    email_exists = True
                    flash('Correo electrónico ya está en uso', 'danger')
                else:
                    conn.execute('INSERT INTO users (name, lastname, phone, email, password) VALUES (?, ?, ?, ?, ?)', 
                                 (name, lastname, phone, email, password))
                    conn.commit()
                    flash('Registro exitoso!', 'success')
                    print('Usuario registrado correctamente:', email)
                    return redirect(url_for('login'))
            except sqlite3.Error as e:
                print('Error al registrar usuario:', e)
                flash('Error al registrar usuario', 'danger')
            finally:
                conn.close()
        else:
            flash('Error de conexión a la base de datos', 'danger')
    return render_template('register.html', email_exists=email_exists)

@app.route('/check_email_availability', methods=['POST'])
def check_email_availability():
    email = request.json['email']
    conn = get_db_connection()
    user_exists = conn.execute('SELECT 1 FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    return jsonify({'available': not user_exists})

# Clase User para Flask-Login
class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password

# Cargar usuario
@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return User(user['id'], user['email'], user['password'])
    return None

@app.route('/contacto.html')
def contacto():
    return render_template('contacto.html')

@app.route('/menu.html')
@login_required
def menu():
    return render_template('menu.html')

# Ruta para renderizar la página panel-refugios.html y mostrar los refugios
@app.route('/panelrefugios.html')
@login_required
def panel_refugios():
    conn = get_db_connection()
    refugios = conn.execute('SELECT * FROM refugios').fetchall()
    conn.close()
    return render_template('panelrefugios.html', refugios=refugios)

# Ruta para agregar un refugio
@app.route('/agregar_refugio', methods=['POST'])
@login_required
def agregar_refugio():
    nombre = request.form['nombre']
    direccion = request.form['direccion']
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO refugios (nombre, direccion) VALUES (?, ?)', (nombre, direccion))
        conn.commit()
        flash('Refugio agregado correctamente', 'success')
    except sqlite3.Error as e:
        print('Error al agregar refugio:', e)
        flash('Error al agregar refugio', 'danger')
    finally:
        conn.close()
    return redirect(url_for('panel_refugios'))

# Ruta para modificar un refugio
@app.route('/modificar_refugio/<int:refugio_id>', methods=['POST'])
@login_required
def modificar_refugio(refugio_id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        conn = get_db_connection()
        try:
            conn.execute('UPDATE refugios SET nombre = ?, direccion = ? WHERE id = ?', (nombre, direccion, refugio_id))
            conn.commit()
            flash('Refugio modificado correctamente', 'success')
        except sqlite3.Error as e:
            print('Error al modificar refugio:', e)
            flash('Error al modificar refugio', 'danger')
        finally:
            conn.close()
        return redirect(url_for('panel_refugios'))

# Ruta para eliminar un refugio
@app.route('/eliminar_refugio/<int:refugio_id>')
@login_required
def eliminar_refugio(refugio_id):
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM refugios WHERE id = ?', (refugio_id,))
        conn.commit()
        flash('Refugio eliminado correctamente', 'success')
    except sqlite3.Error as e:
        print('Error al eliminar refugio:', e)
        flash('Error al eliminar refugio', 'danger')
    finally:
        conn.close()
    return redirect(url_for('panel_refugios'))

@app.route('/panelmascotas.html')
@login_required
def panel_mascotas():
    conn = get_db_connection()
    mascotas = conn.execute('SELECT * FROM mascotas').fetchall()
    refugios = conn.execute('SELECT * FROM refugios').fetchall()
    conn.close()
    return render_template('panelmascotas.html', mascotas=mascotas, refugios=refugios)

@app.route('/add_mascota', methods=['POST'])
@login_required
def add_mascota():
    id_refugio = request.form['id_refugio']
    tipo = request.form['tipo']
    nombre = request.form['nombre']
    edad = request.form['edad']
    raza = request.form['raza']
    foto_url = request.form['foto_url']
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO mascotas (id_refugio, tipo, nombre, edad, raza, foto_url) VALUES (?, ?, ?, ?, ?, ?)',
                     (id_refugio, tipo, nombre, edad, raza, foto_url))
        conn.commit()
        flash('Mascota agregada correctamente', 'success')
    except sqlite3.Error as e:
        print('Error al agregar mascota:', e)
        flash('Error al agregar mascota', 'danger')
    finally:
        conn.close()
    return redirect(url_for('panel_mascotas'))

@app.route('/modificar_mascota', methods=['POST'])
@login_required
def modificar_mascota():
    mascota_id = request.form['id']
    id_refugio = request.form['id_refugio']
    tipo = request.form['tipo']
    nombre = request.form['nombre']
    edad = request.form['edad']
    raza = request.form['raza']
    foto_url = request.form['foto_url']
    conn = get_db_connection()
    try:
        conn.execute('UPDATE mascotas SET id_refugio = ?, tipo = ?, nombre = ?, edad = ?, raza = ?, foto_url = ? WHERE id = ?',
                     (id_refugio, tipo, nombre, edad, raza, foto_url, mascota_id))
        conn.commit()
        flash('Mascota modificada correctamente', 'success')
    except sqlite3.Error as e:
        print('Error al modificar mascota:', e)
        flash('Error al modificar mascota', 'danger')
    finally:
        conn.close()
    return redirect(url_for('panel_mascotas'))

@app.route('/eliminar_mascota/<int:mascota_id>', methods=['POST'])
@login_required
def eliminar_mascota(mascota_id):
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM mascotas WHERE id = ?', (mascota_id,))
        conn.commit()
        flash('Mascota eliminada correctamente', 'success')
    except sqlite3.Error as e:
        print('Error al eliminar mascota:', e)
        flash('Error al eliminar mascota', 'danger')
    finally:
        conn.close()
    return redirect(url_for('panel_mascotas'))

# Ruta para obtener los datos de las mascotas
@app.route('/api/mascotas', methods=['GET'])
def get_mascotas():
    conn = get_db_connection()
    mascotas = conn.execute('SELECT * FROM mascotas').fetchall()
    conn.close()
    return jsonify([dict(row) for row in mascotas])

if __name__ == '__main__':
    app.run(debug=True)