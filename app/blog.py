# from flask import Blueprint, render_template, redirect, request
# from flask_login import current_user, login_required 
# 
# from app.models import BlogPost, User
# 
# blog = Blueprint( 'blog', __name__ )
# 
# @blog.route( '/edit/<int:i>' )
# @login_required
# def edit( i ):
#   if i == 0: return redirect( '/editor' )
#   return render_template( 'editor.html', 
#     back=True, 
#     editing=BlogPost.query.get( i ), 
#     posts=BlogPost.query.all() 
#   )
# 
# @blog.route( '/save', methods=['POST'] )
# @login_required
# def save():
#   bid = request.form.get( 'bid' )
#   txt = request.form.get( 'editor' )
#   ttl = request.form.get( 'title' ) or request.form.get( 'prevt' )
# 
#   bp = BlogPost.query.get( bid ) if bid else BlogPost()
#   bp.title = ttl
#   bp.body = txt 
#   bp.visible = request.form.get( 'vis' ) is not None
#   bp.save()
#   return redirect( '/editor' )
# 
# @blog.route( '/delete', methods=['POST'])
# @login_required
# def delete():
#   bid = request.form.get( 'bid' )
#   if bid:
#     BlogPost.query.get( bid ).delete()
#   return edit( 0 )
# 
# @blog.route( '/post/<int:i>' )
# def post( i ):
#   p = BlogPost.query.get( i )
#   return render_template( 'post.html', 
#     back=True, 
#     title=p.title, 
#     body=p.body 
#   )
