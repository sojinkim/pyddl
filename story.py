#!/usr/bin/env python
"""
"""
from __future__ import print_function
from pyddl import Domain, Problem, Action, neg, planner


def problem(verbose):
    domain = Domain((
        Action(
            'walk',
            parameters=(
                ('person', 'p'),
                ('location', 'l1'),
                ('location', 'l2'),
            ),
            preconditions=(
                ('at', 'p', 'l1'),
            ),
            effects=(
                ('at', 'p', 'l2'),
                neg(('at', 'p', 'l1')),
            ),
        ),
        Action(
            'pick_from',
            parameters=(
                ('person', 'p'),
                ('object', 'o1'),
                ('object', 'o2'),
                ('location', 'l'),
            ),
            preconditions=(
                ('at', 'o1', 'l'),
                ('contains', 'o1', 'o2'),
                ('at', 'p', 'l'),
                ('found', 'p', 'o2'),
            ),
            effects=(
                ('has', 'p', 'o2'),
                neg(('contains', 'o1', 'o2')),
            ),
        ),
        Action(
            'look_n_found',
            parameters=(
                ('person', 'p'),
                ('object', 'o1'),
                ('object', 'o2'),
                ('location', 'l'),
            ),
            preconditions=(
                ('at', 'p', 'l'),
                ('at', 'o1', 'l'),
                ('contains', 'o1', 'o2'), 
                ('>=', ('brave', 'p'), 10),
            ),
            effects=(
                ('found', 'p', 'o2'),
            ),
        ),
        Action(
            'sing_for',
            parameters=(
                ('person', 'p1'),
                ('person', 'p2'),
                ('location', 'l'),
            ),
            preconditions=(
                ('at', 'p1', 'l'),
                ('at', 'p2', 'l'),
                ('>=', ('like', 'p1', 'p2'), 10),
                ('>=', ('brave', 'p1'), 10),
            ),
            effects=(
                ('+=', ('delighted', 'p2'), 10),
                ('+=', ('jealousy', 'Jack'), 5),
            ),
        ),
        Action(
            'propose',
            parameters=(
                ('person', 'p1'),
                ('person', 'p2'),
                ('location', 'l'),
            ),
            preconditions=(
                ('at', 'p1', 'l'),
                ('at', 'p2', 'l'),
                ('>=', ('like', 'p1', 'p2'), 10),
                ('>=', ('brave', 'p1'), 10),
            ),
            effects=(
                ('+=', ('like', 'p2', 'p1'), 5),
                ('+=', ('jealousy', 'Jack'), 5),
            ),
        ),
        Action(
            'steal',
            parameters=(
                ('person', 'p1'),
                ('person', 'p2'),
                ('object', 'o'),
                ('location', 'l'),
            ),
            preconditions=(
                ('at', 'p1', 'l'),
                ('at', 'p2', 'l'),
                ('has', 'p2', 'ring'),
                ('>=', ('jealousy', 'p1'), 10),
            ),
            effects=(
                neg(('has', 'p2', 'ring')),
                ('has', 'p1', 'ring'),
                ('+=', ('upset', 'p2'), 5),
            ),
        ),
        Action(
            'give_ring',
            parameters=(
                ('person', 'p1'),
                ('person', 'p2'),
                ('location', 'l'),
            ),
            preconditions=(
                ('has', 'p1', 'ring'),
                ('at', 'p1', 'l'),
                ('at', 'p2', 'l'),
                ('>=', ('like', 'p1', 'p2'), 10),
            ),
            effects=(
                ('wait_accept', 'p1', 'p2', 'l'),
                ('+=', ('happy', 'p2'), 5),
                ('+=', ('jealousy', 'Jack'), 5),
            ),
        ),
        Action(
            'accept_ring',
            parameters=(
                ('person', 'p1'),
                ('person', 'p2'),
                ('location', 'l'),
            ),
            preconditions=(
                ('wait_accept', 'p2', 'p1', 'l'),
                ('has', 'p2', 'ring'),
                ('at', 'p1', 'l'),
                ('at', 'p2', 'l'),
                ('>=', ('like', 'p1', 'p2'), 10),
                ('>=', ('happy', 'p1'), 10),
                ('>=', ('delighted', 'p1'), 10),
            ),
            effects=(
                neg(('has', 'p2', 'ring')),
                ('has', 'p1', 'ring'),
                ('+=', ('happy', 'p2'), 5),
                ('propose_accepted', 'p1', 'p2'),
                ('+=', ('jealousy', 'Jack'), 5),
            ),
        ),
        Action(
            'wisper',
            parameters=(
                ('person', 'p1'),
                ('person', 'p2'),
                ('location', 'l'),
            ),
            preconditions=(
                ('at', 'p1', 'l'),
                ('at', 'p2', 'l'),
                ('>=', ('like', 'p1', 'p2'), 10),
            ),
            effects=(
                ('-=', ('upset', 'p2'), 5),
            ),
        ),
        Action(
            'accept_propose',
            parameters=(
                ('person', 'p1'),
                ('person', 'p2'),
                ('location', 'l'),
            ),
            preconditions=(
                ('at', 'p1', 'l'),
                ('at', 'p2', 'l'),
                ('>=', ('like', 'p1', 'p2'), 10),
                ('>=', ('happy', 'p1'), 10),
                ('>=', ('delighted', 'p1'), 10),
                ('<=', ('upset', 'p1'), 1),
                ('<=', ('jealousy', 'p1'), 1),
            ),
            effects=(
                ('propose_accepted', 'p1', 'p2'),
                ('+=', ('happy', 'p2'), 5),
                ('+=', ('desparate', 'Jack'), 10),
            ),
        ),

    ))
    problem = Problem(
        domain,
        {
            'location': ('loc1', 'loc2', 'loc3', 'loc4'),
            'person': ('Bob', 'Marry', 'Jack'),
            'object': ('ring', 'box', 'bench'),
        },
        init=(
            ('at', 'Bob', 'loc1'),
            ('at', 'Marry', 'loc2'),
            ('at', 'Jack', 'loc3'),
            ('at', 'bench', 'loc2'),
            ('at', 'box', 'loc4'),
            ('contains', 'box', 'ring'),
            ('sit_on', 'Marry', 'bench'),
            ('=', ('like', 'Marry', 'Bob'), 5),
            ('=', ('like', 'Marry', 'Jack'), 1),
            ('=', ('like', 'Bob', 'Marry'), 10),
            ('=', ('like', 'Bob', 'Jack'), 1),
            ('=', ('like', 'Jack', 'Marry'), 10),
            ('=', ('like', 'Jack', 'Bob'), 1),
            ('=', ('like', 'Bob', 'Bob'), -1),
            ('=', ('like', 'Marry', 'Marry'), -1),
            ('=', ('like', 'Jack', 'Jack'), -1),
            ('=', ('happy', 'Bob'), 5),
            ('=', ('happy', 'Marry'), 5),
            ('=', ('happy', 'Jack'), 5),
            ('=', ('brave', 'Bob'), 10),
            ('=', ('brave', 'Marry'), 1),
            ('=', ('brave', 'Jack'), 1),
            ('=', ('delighted', 'Bob'), 5),
            ('=', ('delighted', 'Marry'), 5),
            ('=', ('delighted', 'Jack'), 5),
            ('=', ('jealousy', 'Bob'), 1),
            ('=', ('jealousy', 'Marry'), 1),
            ('=', ('jealousy', 'Jack'), 5),
            ('=', ('desparate', 'Bob'), 1),
            ('=', ('desparate', 'Marry'), 1),
            ('=', ('desparate', 'Jack'), 1),
            ('=', ('upset', 'Bob'), 1),
            ('=', ('upset', 'Marry'), 1),
            ('=', ('upset', 'Jack'), 1),
        ),
        goal=(
#            ('propose_accepted', 'Marry', 'Bob'),
#            ('>=', ('desparate', 'Jack'), 5),
#            ('>=', ('happy', 'Marry'), 10),
#            ('>=', ('happy', 'Bob'), 10),
#            ('has', 'Jack', 'ring'),
             ('has', 'Jack', 'ring'),
             ('>=', ('jealousy', 'Jack'), 10),
             ('>=', ('happy', 'Marry'), 10),
             ('>=', ('happy', 'Bob'), 10),
        )
    )

    plan = planner(problem, verbose=verbose)
    if plan is None:
        print('No Plan!')
    else:
        for action in plan:
            print(action)

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option('-q', '--quiet',
                      action='store_false', dest='verbose', default=True,
                      help="don't print statistics to stdout")

    # Parse arguments
    opts, args = parser.parse_args()
    problem(opts.verbose)
