from flask import Blueprint, request, redirect, url_for, render_template_string
import models

admin_bp = Blueprint("admin", __name__)

base_admin = """
<!doctype html><html lang="uk"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Admin</title>
<link href="https://cdn.tailwindcss.com" rel="stylesheet">
</head><body class="bg-gray-50 min-h-screen">
<div class="container mx-auto p-6">
<a class="text-blue-600" href="/">Назад на сайт</a>
<h1 class="text-2xl font-bold mt-4">Адмін-панель</h1>
<div class="mt-4">
{{ body|safe }}
</div>
</div></body></html>
"""

@admin_bp.route("/")
def admin_index():
    body = """
    <ul class="list-disc pl-5">
        <li><a href="/admin/feedbacks" class="text-blue-600">Відгуки</a></li>
        <li><a href="/admin/products" class="text-blue-600">Товари</a></li>
        <li><a href="/admin/orders" class="text-blue-600">Замовлення</a></li>
        <li><a href="/admin/clients" class="text-blue-600">Клієнти</a></li>
    </ul>
    """
    return render_template_string(base_admin, body=body)

# Feedbacks
@admin_bp.route("/feedbacks")
def feedbacks():
    rows = models.get_feedbacks()
    items = "<h2 class='text-xl'>Відгуки</h2><ul class='mt-4'>"
    for r in rows:
        items += f"<li class='mb-3 p-3 bg-white rounded shadow'><b>{r[1]}</b> ({r[2]})<div class='text-sm text-gray-700'>{r[3]}</div><form method='post' action='/admin/feedbacks/delete/{r[0]}' class='mt-2'><button class='px-2 py-1 bg-red-500 text-white rounded'>Видалити</button></form></li>"
    items += "</ul>"
    return render_template_string(base_admin, body=items)

@admin_bp.route("/feedbacks/delete/<int:fid>", methods=["POST"])
def feedback_delete(fid):
    models.delete_feedback(fid)
    return redirect(url_for("admin.feedbacks"))

# Products
@admin_bp.route("/products", methods=["GET","POST"])
def products():
    message = ""
    if request.method == "POST":
        name = request.form.get("name")
        desc = request.form.get("description")
        price = request.form.get("price") or 0
        stock = request.form.get("stock") or 0
        models.create_product(name, desc, price, stock)
        message = "<div class='text-green-600'>Товар додано</div>"
    rows = models.get_products()
    body = "<h2 class='text-xl'>Товари</h2>"
    body += message
    body += "<form method='post' class='mt-3 mb-4 bg-white p-4 rounded shadow'><input name='name' placeholder='Назва' class='border p-2 w-full mb-2' required><textarea name='description' placeholder='Опис' class='border p-2 w-full mb-2'></textarea><div class='flex gap-2'><input name='price' placeholder='Ціна' class='border p-2' required><input name='stock' placeholder='Кількість' class='border p-2'></div><button class='mt-2 px-3 py-1 bg-blue-600 text-white rounded'>Додати</button></form>"
    for r in rows:
        body += f"<div class='p-3 bg-white rounded shadow mb-2'><b>{r[1]}</b> — {r[3]} грн <div class='text-sm text-gray-600'>{r[2]}</div><form method='post' action='/admin/products/delete/{r[0]}' class='mt-2'><button class='px-2 py-1 bg-red-500 text-white rounded'>Видалити</button></form></div>"
    return render_template_string(base_admin, body=body)

@admin_bp.route("/products/delete/<int:pid>", methods=["POST"])
def product_delete(pid):
    models.delete_product(pid)
    return redirect(url_for("admin.products"))

# Orders
@admin_bp.route("/orders", methods=["GET","POST"])
def orders():
    if request.method == "POST":
        oid = int(request.form.get("order_id"))
        status = request.form.get("status")
        models.update_order_status(oid, status)
    rows = models.get_orders()
    body = "<h2 class='text-xl'>Замовлення</h2>"
    for r in rows:
        items = models.get_order_items(r[0])
        items_html = "<ul>"
        for it in items:
            items_html += f"<li>{it[2]} — {it[3]} шт × {it[4]} грн</li>"
        items_html += "</ul>"
        body += f"<div class='p-3 bg-white rounded shadow mb-3'><b>Замовлення #{r[0]}</b> — {r[3]} грн — статус: {r[2]}{items_html}<form method='post' class='mt-2'><input type='hidden' name='order_id' value='{r[0]}'><select name='status' class='border p-1'><option>pending</option><option>processing</option><option>completed</option><option>cancelled</option></select><button class='ml-2 px-2 py-1 bg-green-600 text-white rounded'>Оновити</button></form></div>"
    return render_template_string(base_admin, body=body)

# Clients
@admin_bp.route("/clients", methods=["GET","POST"])
def clients():
    msg = ""
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        models.create_client(name, email, phone)
        msg = "<div class='text-green-600'>Клієнта додано</div>"
    rows = models.get_clients()
    body = "<h2 class='text-xl'>Клієнти</h2>" + msg
    body += "<form method='post' class='mt-3 mb-4 bg-white p-4 rounded shadow'><input name='name' placeholder='Імʼя' class='border p-2 w-full mb-2'><input name='email' placeholder='Email' class='border p-2 w-full mb-2'><input name='phone' placeholder='Телефон' class='border p-2 w-full mb-2'><button class='px-3 py-1 bg-blue-600 text-white rounded'>Додати клієнта</button></form>"
    for r in rows:
        body += f"<div class='p-3 bg-white rounded shadow mb-2'><b>{r[1]}</b> — {r[2]} — {r[3]}</div>"
    return render_template_string(base_admin, body=body)