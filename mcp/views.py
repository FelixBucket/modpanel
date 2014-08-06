from ttr.util import *

def app(request):
    return render_template(request, 'mcp/app.html', {})