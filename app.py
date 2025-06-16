from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/calculate_inspection', methods=['POST'])
def calculate_inspection():
    try:
        value = float(request.form['shipment_value'])
        fee = 0
        
        if value <= 80000:
            fee = 320
        elif 80000 < value <= 200000:
            fee = 320 + 0.004 * (value - 80000)
        elif 200000 < value <= 1000000:
            fee = 800 + 0.003 * (value - 200000)
        else:
            fee = 3200 + 0.0015 * (value - 1000000)
        
        return render_template('index.html', 
                            inspection_result=f"{fee:.2f}",
                            shipment_value=value,
                            active_tab='inspection')
    except ValueError:
        return render_template('index.html', 
                            error="الرجاء إدخال قيمة صحيحة للشحنة",
                            active_tab='inspection')

@app.route('/divide_certificate', methods=['POST'])
def divide_certificate():
    try:
        cert_value = float(request.form['certificate_value'])
        containers = int(request.form['containers'])
        
        if containers <= 0:
            return render_template('index.html', 
                                error="عدد الحاويات يجب أن يكون أكبر من الصفر",
                                active_tab='division')
        
        per_container = cert_value / containers
        
        # تحديد أجور الحاوية حسب الشروط المطلوبة
        if per_container <= 5000:
            container_fee = 50
        elif 5001 <= per_container <= 10000:
            container_fee = 75
        else:
            container_fee = 100
        
        return render_template('index.html', 
                            division_result=f"{per_container:.2f}",
                            container_fee=container_fee,
                            certificate_value=cert_value,
                            containers=containers,
                            active_tab='division')
    except ValueError:
        return render_template('index.html', 
                            error="الرجاء إدخال قيم صحيحة",
                            active_tab='division')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)