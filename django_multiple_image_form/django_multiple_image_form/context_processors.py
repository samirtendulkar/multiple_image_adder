

def sections_processor(request):
    user = request.user
    if user.is_authenticated:
        drafts = user.posts.filter(is_draft=True).count()
    else:
        drafts = ''
    return {'drafts': drafts}

