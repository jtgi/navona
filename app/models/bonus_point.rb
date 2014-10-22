require "navona"

class BonusPoint < ActiveRecord::Base
  def update_points
    bonus_points = Navona.execute
    BonusPoint.create({points: bonus_points})
  end
end
