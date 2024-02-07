# College Basketball NET API

An API which scrapes the publicly available NET evaluation rankings from the NCAA's website and allows for JSON access of the current rankings stored there.

Sample usage:
```
import net

net.get_rankings()
net.get_top_n_rankings(20)
net.get_conference_rankings('Mountain West')
net.get_school('Pittsburgh')
```
