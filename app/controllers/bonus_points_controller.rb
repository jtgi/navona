class BonusPointsController < ApplicationController
  def index
    render json: BonusPoint.all
  end

  def current
    @bonus_points = BonusPoint.order("created_at DESC").first
    if @bonus_points
      @remaining_until_party = 256 - @bonus_points.points
      render 'current'
    else
      render json: { error: "no bonus points..." }
    end
  end

end
