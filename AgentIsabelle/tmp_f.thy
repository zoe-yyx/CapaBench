theory TeachersAndChildren
  imports Main
begin

lemma teachers_and_children:
  fixes MT FT MC FC :: int
  assumes "MT > 0"
    and "FT > 0"
    and "MC > 0"
    and "FC > 0"
    and "MT + FT + MC + FC = 16"
    and "MC + FC > MT + FT"
    and "FT > FC"
    and "FC > MC"
    and "MC > MT"
  shows "MT = 1"
proof -
  have "MT + FT + MC + FC = 16" by assumption
  then have "4 ≤ MT" and "4 ≤ FT" and "4 ≤ MC" and "4 ≤ FC" by linarith
  have "MC + FC > MT + FT" by assumption
  then have "MC + FC - (MT + FT) > 0" by simp
  then have "MC + FC - (MT + FT) ≥ 1" by linarith
  have "FT > FC" by assumption
  then have "FT ≥ 2" by linarith
  have "FC > MC" by assumption
  then have "FC ≥ 2" by linarith
  have "MC > MT" by assumption
  then have "MC ≥ 2" by linarith
  have "MT + FT + MC + FC = 16" by assumption
  then have "MT + FT + MC + FC - (MT + FT + MC + FC) = 0" by algebra
  then have "0 = MT + FT + MC + FC - (MT + FT + MC + FC)" by simp
  then have "0 = 16 - 16" by simp
  then have "0 = 0" by simp
  then have "True" by simp
  then show "MT = 1" by linarith
qed
end
