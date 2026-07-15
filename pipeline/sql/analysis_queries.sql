select jr.role, js.skill, count(distinct js.job_id) as posting_count
from job_roles jr join job_skills js on js.job_id = jr.job_id
group by jr.role, js.skill
order by jr.role, posting_count desc, js.skill;

select c.cluster, c.cluster_label, count(*) as posting_count
from job_clusters c
group by c.cluster, c.cluster_label
order by posting_count desc;
