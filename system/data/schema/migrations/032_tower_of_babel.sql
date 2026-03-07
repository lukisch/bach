-- TOWER_OF_BABEL v3.7.1: Mehrsprachigkeit fuer Content-Tabellen
-- Fuegt language-Spalte zu bach_agents, bach_experts, skills, wiki_articles, tools hinzu

-- bach_agents: language Spalte
ALTER TABLE bach_agents ADD COLUMN language TEXT DEFAULT 'de';

-- bach_experts: language Spalte
ALTER TABLE bach_experts ADD COLUMN language TEXT DEFAULT 'de';

-- skills: language Spalte
ALTER TABLE skills ADD COLUMN language TEXT DEFAULT 'de';

-- wiki_articles: language Spalte
ALTER TABLE wiki_articles ADD COLUMN language TEXT DEFAULT 'de';

-- tools: language Spalte (niedrigste Prio, aber Schema schon vorbereiten)
ALTER TABLE tools ADD COLUMN language TEXT DEFAULT 'de';
