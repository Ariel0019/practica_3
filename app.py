from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simulación de base de datos
registrants = []

@app.route('/')
def index():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtener los datos del formulario
        name = request.form['name']
        surname = request.form['surname']
        date = request.form['date']
        time_slot = request.form['time_slot']
        seminars = request.form.getlist('seminars')

        # Verificar si es una edición
        edit_index = request.form.get('edit_index')
        if edit_index and edit_index.isdigit():
            # Actualizar el registro existente
            registrants[int(edit_index)] = {
                'name': name,
                'surname': surname,
                'date': date,
                'time_slot': time_slot,
                'seminars': ', '.join(seminars)
            }
        else:
            # Agregar el nuevo registro
            registrants.append({
                'name': name,
                'surname': surname,
                'date': date,
                'time_slot': time_slot,
                'seminars': ', '.join(seminars)
            })

        return redirect(url_for('list_registrants'))

    return render_template('register.html')


@app.route('/edit/<int:index>', methods=['GET'])
def edit(index):
    # Obtener los datos del registro a editar
    registrant = registrants[index]
    return render_template('register.html', registrant=registrant, edit_index=index)



@app.route('/list')
def list_registrants():
    return render_template('list.html', registrants=registrants, enumerate=enumerate)

@app.route('/delete/<int:index>', methods=['POST'])
def delete(index):
    if 0 <= index < len(registrants):
        # Eliminar el registro correspondiente
        del registrants[index]
    return redirect(url_for('list_registrants'))



if __name__ == '__main__':
    app.run(debug=True)
