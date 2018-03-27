python -m cProfile -o profile_output.txt manage.py test OnToology
python << END
import pstats
p = pstats.Stats('profile_output.txt')
p.sort_stats('cumulative').print_stats('OnToology*')
END

