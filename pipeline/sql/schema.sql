create table jobs (job_id text primary key, title text not null, company text, location text, posted_at text, description text not null, source text not null, source_url text);
create table job_roles (job_id text not null, role text not null);
create table job_skills (job_id text not null, skill text not null);
create table job_clusters (job_id text not null, cluster integer not null, cluster_label text not null);
