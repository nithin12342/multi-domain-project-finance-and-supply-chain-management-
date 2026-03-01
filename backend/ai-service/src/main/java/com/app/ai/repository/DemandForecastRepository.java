package com.app.ai.repository;

import com.app.ai.model.DemandForecast;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface DemandForecastRepository extends JpaRepository<DemandForecast, Long> {
    List<DemandForecast> findByProductIdAndForecastDateBetween(String productId, LocalDateTime startDate, LocalDateTime endDate);
    List<DemandForecast> findByProductId(String productId);
    List<DemandForecast> findByPeriodOrderByForecastDateDesc(String period);
    List<DemandForecast> findByForecastDateAfterOrderByForecastDateDesc(LocalDateTime date);
}