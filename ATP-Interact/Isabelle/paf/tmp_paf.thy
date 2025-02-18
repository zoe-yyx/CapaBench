
(* Correcting the theory tmp_paf in the import statement *)
theory OrIntror
  imports Main Classical.Intro
begin

lemma or_intror:
  fixes A B :: "bool"
  assumes H: "B"
  shows "A <or> B"
proof (rule disj_intro)
  assume A
  show ?thesis
  apply H
qed
end
