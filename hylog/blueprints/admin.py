from flask import render_template, redirect, url_for, request, current_app, Blueprint, flash
from flask_login import login_required
from hylog.forms import SettingForm, PostForm, CategoryForm, LinkForm
from hylog.utils import redirect_back
from hylog.extensions import db
from hylog.models import Post, Category, Comment

admin_bp = Blueprint('admin', __name__)


# TODO
# 可以如下给admin_bp蓝图注册before_request则可以省略给每个函数加login_required
# @admin_bp.before_request
# @login_required
# def login_protect():
#     pass

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingForm()
    return render_template('admin/settings.html', form=form)


@admin_bp.route('/post/manage')
@login_required
def manage_post():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['HYLOG_MANAGE_POST_PER_PAGE'])
    posts = pagination.items
    return render_template('admin/manage_post.html', pagination=pagination, posts=posts)


@admin_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        category = Category.query.get(form.category.data)
        post = Post(title=title, content=content, category=category)
        db.session.add(post)
        db.session.commit()
        flash('添加日志成功。', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    return render_template('admin/new_post.html', form=form)


@admin_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = Category.query.get(form.category.data)
        db.session.commit()
        flash('日志编辑成功。', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    form.title.data = post.title    # 预定义表单中的title字段值
    form.content.data = post.content    # 预定义表单中的content字段值
    form.category.data = post.category_id
    return render_template('admin/edit_post.html', form=form)


@admin_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('日志已成功删除。', 'success')
    return redirect_back()


@admin_bp.route('/post/<int:post_id>/set-comment', methods=['POST'])
@login_required
def set_comment(post_id):
    post = Post.query.get_or_404(post_id)
    if post.can_comment:
        post.can_comment = False
        flash('禁止评论。', 'info')
    else:
        post.can_comment = True
        flash('开启评论。', 'info')
    db.session.commit()
    return redirect(url_for('blog.show_post', post_id=post_id))


@admin_bp.route('/comment/manage')
@login_required
def manage_comment():
    filter_rule = request.args.get('filter', '全部')  # 从查询字符串获取过滤规则 'all', 'unreviewed', 'admin'
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['HYLOG_COMMENT_PER_PAGE']
    if filter_rule == '未审核':
        filtered_comments = Comment.query.filter_by(reviewed=False)
    elif filter_rule == '管理员':
        filtered_comments = Comment.query.filter_by(from_admin=True)
    else:
        filtered_comments = Comment.query
    pagination = filtered_comments.order_by(Comment.timestamp.desc()).paginate(page, per_page=per_page)
    comments = pagination.items
    return render_template('admin/manage_comment.html', comments=comments, pagination=pagination)


@admin_bp.route('/comment/<int:comment_id>/approve', methods=['POST'])
@login_required
def approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.reviewed = True
    db.session.commit()
    flash('评论审核通过。', 'success')
    return redirect_back()


@admin_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    return redirect_back()


@admin_bp.route('/category/manage')
@login_required
def manage_category():
    return render_template('admin/manage_category.html')


@admin_bp.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    return render_template('admin/new_category.html', form=form)


@admin_bp.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    form = CategoryForm()
    return render_template('admin/edit_category.html', form=form)


@admin_bp.route('/category/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.id == 1:    # 判断是默认分类的话不能删除
        flash('You can not delete the default category.', 'warning')
        return redirect(url_for('blog.index'))
    category.delete()   # 调用category对象的delete()方法删除分类
    flash('Category deleted.', 'success')
    return redirect(url_for('.manage_category'))


@admin_bp.route('/link/manage')
@login_required
def manage_link():
    return render_template('admin/manage_link.html')


@admin_bp.route('/link/new', methods=['GET', 'POST'])
@login_required
def new_link():
    form = LinkForm()
    return render_template('admin/new_link.html', form=form)


@admin_bp.route('/link/<int:link_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_link(link_id):
    form = LinkForm()
    return render_template('admin/edit_link.html', form=form)


@admin_bp.route('/link/<int:link_id>/delete', methods=['POST'])
@login_required
def delete_link(link_id):
    return redirect(url_for('.manage_link'))