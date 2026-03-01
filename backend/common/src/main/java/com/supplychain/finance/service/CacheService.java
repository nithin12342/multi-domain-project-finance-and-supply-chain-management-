package com.supplychain.finance.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.TimeUnit;

@Service
public class CacheService {

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    // Invoice caching
    @Cacheable(value = "invoices", key = "#invoiceId")
    public Object getInvoice(String invoiceId) {
        // This method will be cached
        return null; // Implementation would fetch from database
    }

    @CacheEvict(value = "invoices", key = "#invoiceId")
    public void evictInvoice(String invoiceId) {
        // Evict from cache
    }

    @CacheEvict(value = "invoices", allEntries = true)
    public void evictAllInvoices() {
        // Clear all invoice cache
    }

    // Supplier caching
    @Cacheable(value = "suppliers", key = "#supplierId")
    public Object getSupplier(String supplierId) {
        return null; // Implementation would fetch from database
    }

    // AI prediction caching
    @Cacheable(value = "ai-predictions", key = "#predictionKey")
    public Object getPrediction(String predictionKey) {
        return null; // Implementation would return cached prediction
    }

    public void cachePrediction(String key, Object prediction, int ttlMinutes) {
        redisTemplate.opsForValue().set("ai-predictions:" + key, prediction, (long) ttlMinutes, TimeUnit.MINUTES);
    }

    // Generic cache operations
    public void set(String key, Object value, int ttlMinutes) {
        redisTemplate.opsForValue().set(key, value, (long) ttlMinutes, TimeUnit.MINUTES);
    }

    public Object get(String key) {
        return redisTemplate.opsForValue().get(key);
    }

    public void delete(String key) {
        redisTemplate.delete(key);
    }

    public void deletePattern(String pattern) {
        Set<String> keys = redisTemplate.keys(pattern);
        if (keys != null && !keys.isEmpty()) {
            redisTemplate.delete(keys);
        }
    }

    // Bulk operations
    public void setMultiple(Map<String, Object> keyValuePairs, int ttlMinutes) {
        redisTemplate.opsForValue().multiSet(keyValuePairs);

        // Set TTL for each key
        for (String key : keyValuePairs.keySet()) {
            redisTemplate.expire(key, (long) ttlMinutes, TimeUnit.MINUTES);
        }
    }

    public List<Object> getMultiple(List<String> keys) {
        return redisTemplate.opsForValue().multiGet(keys);
    }

    // Cache statistics
    public Long getCacheSize(String pattern) {
        Set<String> keys = redisTemplate.keys(pattern);
        if (keys == null) {
            return 0L;
        }
        return (long) keys.size();
    }

    public Long getDatabaseSize() {
        if (redisTemplate.getConnectionFactory() != null) {
            return redisTemplate.getConnectionFactory().getConnection().dbSize();
        }
        return 0L;
    }
}
