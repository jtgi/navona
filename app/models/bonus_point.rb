require "navona"

class BonusPoint < ActiveRecord::Base
  def self.update_points
    bonus_points = Navona.execute
    if bonus_points > 2
      BonusPoint.create({points: bonus_points})
    end
  end
end
