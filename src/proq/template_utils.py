from marko.ext.gfm import gfm
from jinja2 import Environment, PackageLoader, select_autoescape

package_env = Environment(
        loader=PackageLoader("proq", "templates"),
        autoescape=select_autoescape()
    )
package_env.filters["gfm"] = gfm.convert

